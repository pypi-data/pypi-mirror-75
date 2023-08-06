import torch.nn as nn
import torch
from torch.autograd import Variable

class EvoNorm(nn.Module):
    def __init__(self):
        super(EvoNorm, self).__init__()
        self.relu = nn.ReLU()

    def create_params(self,net):
        shape = net.view(net.size(0), -1).size()[1:]
        self.gamma = torch.ones(shape)
        self.beta = torch.zeros(shape)
        self.gamma = Variable(self.gamma).cuda()
        self.beta = Variable(self.beta).cuda()
        self.gamma = self.gamma.view([1]+list(net.shape[1:]))
        self.beta = self.beta.view([1]+list(net.shape[1:]))
        self.v = torch.ones_like(self.gamma)
        self.v = Variable(self.v).cuda()

    def group_std(self,net):
        size = net.size()
        assert (len(size) == 4)
        N, C, H, W = size
        group_count = 32
        groups = net.view(N, group_count, C//group_count, H, W)
        var = torch.std(groups, [2,3,4], keepdim=True)
        var = var.view(N, -1, 1, 1).repeat(1,C//group_count,H,W)
        return torch.sqrt(var + 1e-8)

    def forward(self, net, epsilon=1e-5):
        if not hasattr(self, 'gamma'):
            self.create_params(net)
        num = net * self.relu(self.v+net)
        result = num / self.group_std(net) 
        result *= self.gamma 
        result += self.beta
        return result
