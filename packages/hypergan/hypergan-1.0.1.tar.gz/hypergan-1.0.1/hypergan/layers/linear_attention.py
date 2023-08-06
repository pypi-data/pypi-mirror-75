import math
import hypergan as hg
import torch
import torch.nn as nn

from hypergan.layer_shape import LayerShape

class LinearAttention(hg.Layer):
    def __init__(self, component, args, options):
        super(LinearAttention,self).__init__(component, args, options)
        input_size = component.current_size.size()
        output_size = args[0]

        self.heads = options.heads or 4
        self.query = nn.Linear(input_size, input_size).cuda()
        self.key = nn.Linear(input_size, input_size).cuda()
        self.value = nn.Linear(input_size, input_size).cuda()
        self.out = nn.Linear(input_size, output_size).cuda()
        self.eps = torch.tensor(1e-12).cuda()
        self.size = LayerShape(output_size)
        if 'w' in component.layer_output_sizes:
            self.style = nn.Linear(component.layer_output_sizes['w'].size(), output_size).cuda() 

        component.nn_init(self.query, options.initializer)
        component.nn_init(self.key, options.initializer)
        component.nn_init(self.value, options.initializer)
        component.nn_init(self.out, options.initializer)

    def elu_feature_map(self, x):
        return torch.nn.functional.elu(x) + 1

    def forward(self, x, context):
        queries = self.query(x)
        keys = self.key(x)
        values = self.value(x)
        if 'w' in context:
            style = self.style(context['w'])
        else:
            style = None
        N, L = queries.shape
        D = 1
        _, S = keys.shape
        H = self.heads
        Q = self.elu_feature_map(queries.view(N, L, H, -1))
        K = self.elu_feature_map(keys.view(N, L, H, -1))
        V = values.view(N, L, H, -1)
        KV = torch.einsum("nshd,nshm->nhmd", K, V)
        Z = 1/(torch.einsum("nlhd,nhd->nlh", Q, K.sum(dim=1))+self.eps)
        if 'w' in context:
            print("size", KV.shape, style.shape, K.shape, V.shape)
            V = torch.einsum("nlhd,nhmd,nlh->nlhm", Q, KV, Z)*style
        else:
            V = torch.einsum("nlhd,nhmd,nlh->nlhm", Q, KV, Z)

        return self.out(V.contiguous().view(x.shape))

    def output_size(self):
        return self.size
