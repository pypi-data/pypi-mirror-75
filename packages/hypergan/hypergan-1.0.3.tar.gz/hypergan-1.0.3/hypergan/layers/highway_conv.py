import torch.nn as nn
import hypergan as hg

class HighwayConv(hg.Layer):
    def __init__(self, component, args, options):
        super(HighwayConv, self).__init__(component, args, options)
        self.size = component.current_size

        self.gate =  nn.Conv2d(self.size.channels, self.size.channels, 1, 1, padding = (0, 0))
        self.conv =  nn.Conv2d(self.size.channels, self.size.channels, 1, 1, padding = (0, 0))
        
        self.relu = nn.Tanh()
        self.sigmoid = nn.Sigmoid()

    def output_size(self):
        return self.size

    def forward(self, input, context):
        unactivated = self.conv(input)
        activated = self.relu(unactivated)
        gated = self.sigmoid(self.gate(input))
        return gated * activated + (1 - gated) * unactivated
