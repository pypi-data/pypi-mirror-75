import torch.nn as nn
import torch

class Zeros(nn.Module):
    def __init__(self, shape):
        super(Zeros, self).__init__()
        self.zeros = torch.zeros(shape).cuda()

    def forward(self, net):
        return self.zeros
