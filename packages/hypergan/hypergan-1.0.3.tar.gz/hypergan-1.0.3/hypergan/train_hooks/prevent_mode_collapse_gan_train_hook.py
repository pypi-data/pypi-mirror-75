import torch
import hyperchamber as hc
from hypergan.train_hooks.base_train_hook import BaseTrainHook

class PreventModeCollapseGanTrainHook(BaseTrainHook):
  def __init__(self, gan=None, config=None, trainer=None):
      super().__init__(config=config, gan=gan, trainer=trainer)

  def forward(self):
      if self.config.latent == "source":
          l1 = self.gan.latent.source.instance
          l2 = self.gan.latent.source.next()
      else:
          l1 = self.gan.latent.z
          l2 = self.gan.latent.next()
      g1 = self.gan.generator(l1)
      if self.config.detach:
          g1 = g1.detach()
      g2 = self.gan.generator(l2)
      D = self.gan.discriminator

      d_real = D(g1)
      d_fake = D(g2)

      _, g_diversity = self.gan.loss.forward(d_real, d_fake)
      if self.config.diversity == "d_loss":
          g_diversity = _
      if self.config.gamma:
          g_diversity = self.config.gamma * g_diversity
      self.gan.add_metric("g_diversity", g_diversity)
      if self.config.diversity_only:
          return [None, g_diversity]

      d_loss, g_loss = self.gan.loss.forward(self.gan.d_real, d_fake)

      return [d_loss, g_diversity+g_loss]
