from hypergan.samplers.base_sampler import BaseSampler
from hypergan.gan_component import ValidationException, GANComponent

import numpy as np
import time

class EncoderSampler(BaseSampler):
    def __init__(self, gan, samples_per_row=8):
        BaseSampler.__init__(self, gan, samples_per_row)
        self.inputs = self.gan.inputs.next()
        self.latent = self.gan.latent.next()

    def compatible_with(gan):
        if hasattr(gan, 'encoder'):
            return True
        return False

    def _sample(self):
        #self.inputs = self.gan.inputs.next(0).clone().detach()
        g = self.gan.generator.forward(self.latent)
        x_e = self.gan.encoder.forward(self.inputs)
        x = self.gan.generator.forward(x_e)
        e = self.gan.encoder.forward(g)
        g2 = self.gan.generator.forward(e)
        print("shape", g.shape, g2.shape, self.inputs.shape)
        return [
            ('input', self.inputs),
            ('re_encoding', x),
            ('generator', g),
            ('generator2', g2)
        ]

