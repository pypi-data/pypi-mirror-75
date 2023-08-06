import math
import torch
import torch.nn as nn

import torch.nn.functional as F

class StyledConv2d(nn.Module):
    def __init__(
            self,
            in_channel,
            out_channel,
            kernel_size,
            style_size,
            demodulate=True,
            upsample=True,
            downsample=False,
            lr_mul=1.0,
            blur_kernel=[1, 3, 3, 1],
            ):

        super(StyledConv2d, self).__init__()
        self.in_channel = in_channel
        self.out_channel = out_channel
        self.kernel_size = kernel_size
        fan_in = in_channel * kernel_size ** 2
        self.scale = 1 / math.sqrt(fan_in)
        self.padding = kernel_size // 2
        self.weight = nn.Parameter(
            torch.randn(out_channel, in_channel, kernel_size, kernel_size)
        )
        self.beta = nn.Linear(style_size, self.in_channel)

    def forward(self, input, style):
        batch, in_channel, height, width = input.shape
        weight = self.scale * self.weight
        #print("shape", batch, weight.shape, self.beta(style).view(batch, self.out_channel, self.kernel_size, self.kernel_size).shape)
        weight += self.beta(style)[0].view(1, self.in_channel, 1, 1)
        out = F.conv2d(input, weight, padding=self.padding)

        return out

