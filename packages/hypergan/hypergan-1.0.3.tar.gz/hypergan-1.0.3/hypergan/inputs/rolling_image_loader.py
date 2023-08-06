from hypergan.gan_component import ValidationException, GANComponent
import glob
import os
import torch
import torch.utils.data as data
import torchvision

from hypergan.inputs.image_loader import ImageLoader
import numpy as np

class RollingImageLoader(ImageLoader):
    """
    ImageLoader loads a set of images
    """

    def __init__(self, config):
        super(RollingImageLoader, self).__init__(config=config)

    def next(self, index=0):
        if not hasattr(self, 'best_sample'):
            best_sample = super(RollingImageLoader, self).next(index)
            self.mask_good = torch.ones(best_sample.shape).cuda()
            self.mask_bad = torch.ones(best_sample.shape).cuda()
            self.best_sample = best_sample
            self.best_sample = self.next(index)
        prior_best_scores = self.gan.discriminator(self.best_sample)
        if self.config.reverse_replace:
            new_index = torch.argmin(prior_best_scores)
        else:
            new_index = torch.argmax(prior_best_scores)
        new_sample = super(RollingImageLoader, self).next(index)
        new_scores = self.gan.discriminator(new_sample)
        if self.config.reverse_new:
            replace_index = torch.argmin(new_scores)
        else:
            replace_index = torch.argmax(new_scores)
        self.mask_good.fill_(1.0)
        self.mask_good[new_index]=0.0
        self.mask_bad.fill_(0.0)
        self.mask_bad[new_index]=1.0
        new_sample = new_sample[replace_index].view([1, new_sample.shape[1],new_sample.shape[2], new_sample.shape[3]]).repeat([new_sample.shape[0], 1,1,1])

        self.best_sample = self.mask_good * self.best_sample + self.mask_bad * new_sample


        return self.best_sample



