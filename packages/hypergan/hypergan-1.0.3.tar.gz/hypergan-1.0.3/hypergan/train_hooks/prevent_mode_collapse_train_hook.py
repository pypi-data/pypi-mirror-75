# https://arxiv.org/pdf/2001.08873v2.pdf
import torch
import hyperchamber as hc
from functools import reduce
import operator
from hypergan.train_hooks.base_train_hook import BaseTrainHook

class PreventModeCollapseTrainHook(BaseTrainHook):
  def __init__(self, gan=None, config=None, trainer=None):
      super().__init__(config=config, gan=gan, trainer=trainer)
      self.relu = torch.nn.ReLU()

  def forward(self, d_loss, g_loss):
      d_loss = []
      layers = self.gan.discriminator.stored_layers
      if self.config.input == "x":
          self.gan.discriminator(self.gan.inputs.sample)
      if self.config.components:
          layers = []
          for component in self.config.components:
              layers += getattr(self.gan, component).stored_layers
      if self.config.layer:
          layers = [layers[i] for i in self.config.layer]
      for mod, p in layers:
          modstr = str(type(mod))
          if "activation." in modstr or "no_op." in modstr or "flatten." in modstr or "pooling." in modstr:
              continue
          if len(p.shape) == 2 and p.shape[1] == 1:
              continue
          split_batch = p.split(p.shape[0])[0]
          for i,s1 in enumerate(split_batch):
              for s2 in split_batch[i+1:]:
                  maxd = self.config.d * reduce(operator.mul, s2.shape)
                  diff = torch.clamp(torch.abs(s1 - s2), max=self.config.d).sum()
                  d_loss += [self.relu(maxd - diff)]

      d_loss = sum(d_loss)
      self.gan.add_metric("diversity_loss", d_loss)
      if self.config.loss == "d":
          self.gan.add_metric("d_diversity_loss", d_loss)
          return [d_loss, None]
      return [None, d_loss]
