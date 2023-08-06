import torch.nn as nn
import torch

class Hardsigmoid(nn.Module):
    def __init__(self):
        super().__init__()
        self.zero = torch.Tensor([0.0]).cuda()
        self.one = torch.Tensor([1.0]).cuda()

    def forward(self, input):
        return torch.min(torch.max(input, self.zero), self.one)
