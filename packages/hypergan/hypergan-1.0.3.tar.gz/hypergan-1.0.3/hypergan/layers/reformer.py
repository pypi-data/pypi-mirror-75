import torch.nn as nn
from hypergan.layer_shape import LayerShape
import hypergan as hg

class Reformer(hg.Layer):
    """ https://github.com/lucidrains/reformer-pytorch """
    def __init__(self, component, args, options):
        super(Reformer, self).__init__(component, args, options)
        dims = list(component.current_size.dims).copy()
        self.size = LayerShape(*dims)
        from reformer_pytorch import LSHSelfAttention
        bucket_size = dims[1]*dims[2] // 2
        while bucket_size > 140:
            bucket_size //= 2
        self.reformer = LSHSelfAttention(
                    dim = dims[0],
                    heads = 1,
                    n_hashes = 2,
                    causal = False,
                    bucket_size = bucket_size
                ).cuda()


    def output_size(self):
        return self.size

    def forward(self, input, context):
        rinp = input.view(input.shape[0], input.shape[1], input.shape[2]*input.shape[3]).transpose(1,2)
        return self.reformer(rinp).view(input.shape)
