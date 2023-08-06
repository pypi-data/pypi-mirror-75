from .base_gan import BaseGAN
from hyperchamber import Config
from hypergan.discriminators import *
from hypergan.distributions import *
from hypergan.gan_component import ValidationException, GANComponent
from hypergan.generators import *
from hypergan.inputs import *
from hypergan.samplers import *
from hypergan.trainers import *
import copy
import hyperchamber as hc
import hypergan as hg
import importlib
import json
import numpy as np
import os
import sys
import time
import torch
import uuid


class EncoderGAN(BaseGAN):
    """ 
    """
    def __init__(self, *args, **kwargs):
        BaseGAN.__init__(self, *args, **kwargs)

    def create(self):
        self.latent = self.create_component("latent")
        self.x = self.inputs.next()[0]
        self.z = self.latent.next()
        self.generator = self.create_component("generator", input=self.latent)
        self.encoder = self.create_component("encoder", input=self.x)
        self.discriminator = self.create_component("discriminator")
        self.discriminator2 = self.create_component("z_discriminator", input=self.latent)
        self.loss = self.create_component("loss")
        self.trainer = self.create_component("trainer")

    def forward_discriminator(self, inputs):
        return self.discriminator(inputs[0]) + self.discriminator2(inputs[1])

    def forward_pass(self):
        self.x = self.inputs.next()
        self.z = self.latent.next()
        g = self.generator(self.z)
        e = self.encoder(g)
        self.g = g
        self.e = e
        d_real = self.forward_discriminator([self.x, self.z])
        d_fake = self.forward_discriminator([self.g, self.e])
        self.d_fake = d_fake
        self.d_real = d_real
        return d_real, d_fake

    def discriminator_components(self):
        return [self.discriminator, self.discriminator2]

    def generator_components(self):
        return [self.generator, self.encoder]

    def discriminator_fake_inputs(self, discriminator_index=0):
        return [self.g, self.e]

    def discriminator_real_inputs(self, discriminator_index=0):
        if hasattr(self, 'x'):
            return [self.x, self.z]
        else:
            return [self.inputs.next(), self.latent.next()]
