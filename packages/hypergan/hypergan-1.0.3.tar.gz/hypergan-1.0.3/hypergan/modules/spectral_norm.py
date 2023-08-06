import torch
from torch.optim.optimizer import Optimizer, required

from torch.autograd import Variable
import torch.nn.functional as F
from torch import nn
from torch import Tensor
from torch.nn import Parameter

def l2normalize(v, eps=1e-12):
    return v / (v.norm() + eps)


class SpectralNorm(nn.Module):
    def __init__(self, name='weight', power_iterations=1):
        super(SpectralNorm, self).__init__()
        self.name = name
        self.power_iterations = power_iterations

    def forward(self, w):
        if not hasattr(self, '_u'):
            self._make_params(w)

        u = self._u
        v = self._v

        height = w.data.shape[0]
        for _ in range(self.power_iterations):
            v.data = l2normalize(torch.mv(torch.t(w.view(height,-1).data), u.data))
            u.data = l2normalize(torch.mv(w.view(height,-1).data, v.data))

        # sigma = torch.dot(u.data, torch.mv(w.view(height,-1).data, v.data))
        sigma = u.dot(w.view(height, -1).mv(v))
        self.w = w / sigma.expand_as(w)
        return self.w

    def _make_params(self, w):
        height = w.data.shape[0]
        width = w.view(height, -1).data.shape[1]

        u = Variable(torch.randn(height), requires_grad=False).cuda()
        v = Variable(torch.randn(width), requires_grad=False).cuda()
        u.data = l2normalize(u.data)
        v.data = l2normalize(v.data)

        self._u = u
        self._v = v
