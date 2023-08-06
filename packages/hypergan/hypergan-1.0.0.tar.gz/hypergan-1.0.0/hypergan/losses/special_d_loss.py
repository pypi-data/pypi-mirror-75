import hyperchamber as hc
import torch

from hypergan.losses.base_loss import BaseLoss

class SpecialDLoss(BaseLoss):
    def __init__(self, gan, config):
        super(BaseLoss, self).__init__(gan, config)
        self.special_discriminator = gan.create_component("special_discriminator")
        self.special_discriminator2 = gan.create_component("special_discriminator")

    def _forward(self, d_real_orig, d_fake_orig):
        criterion = torch.nn.BCEWithLogitsLoss()

        # a1 || d(x)
        # a0 || d(g)
        d_real = -self.special_discriminator(torch.rand_like(d_real_orig))
        d_real += self.special_discriminator(d_real_orig)
        d_real -= self.special_discriminator2(torch.randn_like(d_fake_orig))
        d_real += self.special_discriminator2(d_fake_orig)

        d_fake = -self.special_discriminator(torch.rand_like(d_fake_orig))
        d_fake += self.special_discriminator(d_fake_orig)
        d_fake -= self.special_discriminator2(torch.randn_like(d_real_orig))
        d_fake += self.special_discriminator2(d_real_orig)

        g_loss = -d_fake + d_real
        d_loss = -d_real + d_fake

        return [d_loss, g_loss]
