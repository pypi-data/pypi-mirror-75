import torch.nn as nn
from hypergan.layer_shape import LayerShape
import hypergan as hg
import torch
import math

class Attention(hg.Layer):
    """ Self attention Layer from https://github.com/heykeetae/Self-Attention-GAN/blob/master/sagan_models.py """
    def __init__(self, component, args, options):
        super(Attention, self).__init__(component, args, options)
        self.dims = list(component.current_size.dims).copy()
        in_dim = self.dims[0]
        out_dim = in_dim
        if(len(args) > 0):
            out_dim = args[0]
        heads = options.heads or 4
        features = options.features or in_dim
        self.query = nn.Conv2d(in_channels = in_dim , out_channels = features, kernel_size= 1)
        self.key = nn.Conv2d(in_channels = in_dim , out_channels = features, kernel_size= 1)
        self.value = nn.Conv2d(in_channels = in_dim , out_channels = features, kernel_size= 1)
        self.out = nn.Conv2d(in_channels = in_dim, out_channels = out_dim, kernel_size= 1)
        self.size = LayerShape(*self.dims)
        self.heads = heads
        self.features = features
        self.in_dim = in_dim
        self.elu = nn.ELU()
        self.one = torch.tensor(1.0).cuda()
        self.eps = torch.tensor(1e-12).cuda()
        component.nn_init(self.query, options.initializer)
        component.nn_init(self.key, options.initializer)
        component.nn_init(self.value, options.initializer)
        component.nn_init(self.out, options.initializer)

        self.softmax  = nn.Softmax(dim=1) #

    def output_size(self):
        return self.size

    def forward(self, input, context):
        x = input
        m_batchsize,C,width ,height = x.size()
        H = self.heads
        L = self.features // self.heads
        S = self.features // self.heads
        N = x.shape[0]
        f = self.query(x).view(N, L, H, -1)
        g = self.key(x).view(N, S, H, -1)
        h = self.value(x).view(N, S, H, -1)

        Q = self.feature_map(f)
        K = self.feature_map(g)

        # Compute the KV matrix, namely the dot product of keys and values so
        # that we never explicitly compute the attention matrix and thus
        # decrease the complexity
        KV = torch.einsum("nshd,nshm->nhmd", K, h)

        # Compute the normalizer
        Z = 1/(torch.einsum("nlhd,nhd->nlh", Q, K.sum(dim=1))+self.eps)

        # Finally compute and return the new values
        V = torch.einsum("nlhd,nhmd,nlh->nlhm", Q, KV, Z)
        o = self.out(V.contiguous().view(x.shape))
        return o

    def feature_map(self, x):
        return self.elu(x) + self.one
