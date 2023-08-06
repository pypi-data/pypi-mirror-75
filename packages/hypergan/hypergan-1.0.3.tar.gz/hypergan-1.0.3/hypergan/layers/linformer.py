import torch.nn as nn
from hypergan.layer_shape import LayerShape
import hypergan as hg
import torch
import math

class Linformer(hg.Layer):
    """ Linformer: Self-Attention with Linear Complexity https://arxiv.org/pdf/2006.04768.pdf """
    def __init__(self, component, args, options):
        super(Linformer, self).__init__(component, args, options)
        self.channels = args[0]
        self.k = options.k
        self.dims = list(component.current_size.dims).copy()
        in_dim = self.dims[0]
        self.heads = options.heads or 4
        self.features = in_dim // self.heads
        self.features_sqrt = torch.tensor(math.sqrt(self.features)).cuda()
        padding = (0,0)
        if options.padding is not None:
            padding = (options.padding, options.padding)

        self.f = nn.Conv2d(in_channels = in_dim , out_channels = in_dim, kernel_size=1, padding=0) 
        self.g = nn.Conv2d(in_channels = in_dim , out_channels = in_dim, kernel_size=1, padding=0)
        self.h = nn.Conv2d(in_channels = in_dim , out_channels = in_dim, kernel_size=1, padding=0)
        self.v = nn.Conv2d(in_channels = in_dim , out_channels = self.channels , kernel_size= 1, padding=0)
        self.k1 = nn.Conv2d(in_channels = self.dims[1] * self.dims[2] , out_channels = self.k, kernel_size= 1, padding=0)
        self.k2 = nn.Conv2d(in_channels = self.dims[1] * self.dims[2] , out_channels = self.k , kernel_size= 1, padding=0)
        if options.style:
            style_size = component.layer_output_sizes[options.style].size()
            self.w = nn.Linear(style_size, self.k*self.heads*self.dims[1] * self.dims[2])
            component.nn_init(self.w, options.initializer)

        component.nn_init(self.f, options.initializer)
        component.nn_init(self.g, options.initializer)
        component.nn_init(self.h, options.initializer)
        component.nn_init(self.v, options.initializer)
        component.nn_init(self.k1, options.initializer)
        component.nn_init(self.k2, options.initializer)
        self.softmax  = nn.Softmax(dim=-1) #

    def output_size(self):
        return LayerShape(self.channels, self.dims[1], self.dims[2])

    def forward(self, input, context):
        x = input
        m_batchsize,C,width ,height = x.size()
        f  = self.f(x).view(m_batchsize,self.heads,self.features, width*height).permute(0,1,3,2)

        g =  self.g(x).view(m_batchsize,self.heads, self.features, width*height).permute(0,3,1,2)
        k = self.k1(g).view(m_batchsize, self.k, self.heads, self.features).permute(0,2,3,1)
        fg =  torch.matmul(f,k)
        fg /= self.features_sqrt
        attention_map = self.softmax(fg)
        h = self.h(x).view(m_batchsize,self.heads, self.features,width*height).permute(0,3,1,2)
        k2 = self.k2(h).view(m_batchsize, self.k, self.heads, self.features).permute(0,2,3,1)

        fgh = torch.matmul(k2, attention_map.transpose(2,3) )
        if self.options.style:
            style = context[self.options.style]
            fg *= self.w(style).view(fgh.shape)
        return self.v(fgh.transpose(2,3).contiguous().view(m_batchsize, C, width, height))
