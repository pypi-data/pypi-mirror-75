from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import hyperchamber as hc
import numpy as np
import inspect
import torch
from torch.autograd import Variable
from torch.autograd import grad as torch_grad
import torch.nn as nn
from operator import itemgetter
from hypergan.train_hooks.base_train_hook import BaseTrainHook

class BuresTrainHook(BaseTrainHook):
  """ https://arxiv.org/pdf/2006.09096v1.pdf """
  def __init__(self, gan=None, config=None, trainer=None):
      super().__init__(config=config, gan=gan, trainer=trainer)

  def forward(self, d_loss, g_loss):
      def cov(m, n=None):
          if n is None:
              n = m
          m_exp = torch.mean(m, dim=1)
          x = m - m_exp[:, None]
          n_exp = torch.mean(n, dim=1)
          y = n - n_exp[:, None]
          cov = x.bmm(torch.transpose(y,1,2))
          return cov
      dl = self.gan.d_real_object["activated_layers"][-2]
      gl = self.gan.d_fake_object["activated_layers"][-2]
      dl = dl.view(dl.shape[0], dl.shape[1], 1)
      gl = gl.view(dl.shape[0], dl.shape[1], 1)
      cd = cov(dl)
      cg = cov(gl)
      cd = cd / torch.norm(cd)
      cg = cg / torch.norm(cg)
      cdg = cov(dl, gl)
      cdg = cdg / torch.norm(cdg)
      def sqrt_newton_schulz_autograd(A, numIters, dtype):
          batchSize = A.data.shape[0]
          dim = A.data.shape[1]
          normA = A.mul(A).sum(dim=1).sum(dim=1).sqrt()
          Y = A.div(normA.view(batchSize, 1, 1).expand_as(A));
          I = Variable(torch.eye(dim,dim, device='cuda:0').view(1, dim, dim).
                       repeat(batchSize,1,1).type(dtype),requires_grad=False)
          Z = Variable(torch.eye(dim,dim, device='cuda:0').view(1, dim, dim).
                       repeat(batchSize,1,1).type(dtype),requires_grad=False)

          for i in range(numIters):
             T = 0.5*(3.0*I - Z.bmm(Y))
             Y = Y.bmm(T)
             Z = T.bmm(Z)
          sA = Y*torch.sqrt(normA).view(batchSize, 1, 1).expand_as(A)
          return sA
      inner = cd + cg - 2*sqrt_newton_schulz_autograd(cdg.bmm(torch.transpose(cdg, 1, 2)), 14, cdg.dtype)
      B = self.config.gamma*torch.einsum("ijk,ikj->", inner, inner)
      self.gan.add_metric("B", B)
      return [None, B]
