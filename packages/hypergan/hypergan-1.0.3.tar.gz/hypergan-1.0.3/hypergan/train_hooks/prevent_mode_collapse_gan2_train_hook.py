import torch
import hyperchamber as hc
from hypergan.train_hooks.base_train_hook import BaseTrainHook
from hypergan.gan_component import ValidationException, GANComponent

class PreventModeCollapseGan2TrainHook(BaseTrainHook):
  def __init__(self, gan=None, config=None, trainer=None):
      super().__init__(config=config, gan=gan, trainer=trainer)
      self.gan.discriminator(self.gan.inputs.next())
      layers = self.gan.discriminator.stored_layers
      self.layer_size = layers[self.config.layer][1].shape
      d_conf = hc.Config(hc.lookup_functions(self.config["discriminator"]))
      klass = GANComponent.lookup_function(None, d_conf['class'])
      self.discriminator = klass(self, d_conf).cuda()

  def forward(self, d_loss, g_loss):
      layers = self.gan.discriminator.stored_layers
      gd = self.discriminator(layers[self.config.layer][1])

      self.gan.discriminator(self.gan.inputs.sample)
      layers = self.gan.discriminator.stored_layers
      xd = self.discriminator(layers[self.config.layer][1])

      d_loss, g_loss = self.gan.loss.forward(xd, gd)
      
      self.gan.add_metric("PG2_g_loss", -d_loss*self.config.gamma)
      return [None, -d_loss*self.config.gamma]

  def channels(self):
      return self.layer_size[1]

  def width(self):
      return self.layer_size[3]

  def height(self):
      return self.layer_size[2]

  def configurable_param(self, x):
      return x

  def state_dict(self):
      return {}
