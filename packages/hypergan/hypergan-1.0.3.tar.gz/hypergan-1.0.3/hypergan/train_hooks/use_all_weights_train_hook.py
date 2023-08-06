from copy import deepcopy

import hyperchamber as hc
import numpy as np
import inspect
import torch
from torch.nn.parameter import Parameter
from torch.autograd import grad as torch_grad
import torch.nn as nn
from operator import itemgetter
from hypergan.train_hooks.base_train_hook import BaseTrainHook

class UseAllWeightsTrainHook(BaseTrainHook):
  """ https://faculty.washington.edu/ratliffl/research/2019conjectures.pdf """
  def __init__(self, gan=None, config=None):
      super().__init__(config=config, gan=gan)
      self.d_loss = None
      self.g_loss = None
      self.d_loss_start = torch.zeros(1).float()[0].cuda()
      self.g_loss_start = torch.zeros(1).float()[0].cuda()


  def forward(self, d_loss, g_loss):

      if self.config.skip_after_steps and self.config.skip_after_steps < self.gan.steps:
          return [None, None]

      d_loss = self.gan.trainer.d_loss
      self.d_loss = self.d_loss_start.clone()
      if d_loss is not None:
          d_loss = d_loss.mean()
          #d_params = list(self.gan.d_parameters())
          #d_grads_max = [torch.abs(dg).max() for dg in d_params]
          #self.d_loss += 1e-2 * sum([((torch.abs(dg)-dgm)**2).sum() for dg, dgm in zip(d_params, d_grads_max)])
          #self.gan.add_metric('use_d', self.d_loss)

      skip_g_after_steps = False
      if self.config.skip_g_after_steps:
          skip_g_after_steps = self.config.skip_g_after_steps < self.gan.steps
      skip_g = self.config.skip_g or skip_g_after_steps
      if skip_g:
          return [self.d_loss, None]

      self.g_loss = self.g_loss_start.clone()
      g_loss = self.gan.trainer.g_loss
      if g_loss is not None:
          g_loss = g_loss.mean()
          g_params = list(self.gan.g_parameters())
          g_grads_max = [torch.abs(dg).max() for dg in g_params]
          self.g_loss += 1e-2 * sum([((torch.abs(dg)-dgm)**2).sum() for dg, dgm in zip(g_params, g_grads_max)])
          self.gan.add_metric('use_g', self.g_loss)

      return [self.d_loss, self.g_loss]

