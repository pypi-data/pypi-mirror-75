import torch
import hyperchamber as hc
import numpy as np
import inspect
from operator import itemgetter
from hypergan.train_hooks.base_train_hook import BaseTrainHook
from torch.nn.parameter import Parameter
from torch.autograd import Variable
from torch.autograd import grad as torch_grad

class EmaTrainHook(BaseTrainHook):
    def __init__(self, gan=None, config=None, trainer=None):
        super().__init__(config=config, gan=gan, trainer=trainer)
        self.train_d = True
        if self.config.train_d is not None:
            self.train_d = self.config.train_d
        self.train_g = self.config.train_g or False
        if self.train_d:
            self.d_params = [Parameter(p, requires_grad=False) for p in self.gan.d_parameters()]
            self.d_beta = torch.Tensor([self.config.d_decay or self.config.decay or 0.1]).float()[0].cuda()
        if self.train_g:
            self.g_params = [Parameter(p, requires_grad=False) for p in self.gan.d_parameters()]
            self.g_beta = torch.Tensor([self.config.g_decay or self.config.decay or 0.1]).float()[0].cuda()

    def before_step(self, current_step, feed_dict):
        if self.train_d:
            for sp, p in zip(self.d_params, self.gan.d_parameters()):
                sp.data = p.clone()
        if self.train_g:
            for sp, p in zip(self.g_params, self.gan.g_parameters()):
                sp.data = p.clone()

    def after_step(self, current_step, feed_dict):
        if self.train_d:
            for sp, p in zip(self.d_params, self.gan.d_parameters()):
                p.data = (1.0-self.d_beta) * sp.clone() + self.d_beta * p.data
        if self.train_g:
            for sp, p in zip(self.g_params, self.gan.g_parameters()):
                p.data = (1.0-self.g_beta) * sp.clone() + self.g_beta * p.data
