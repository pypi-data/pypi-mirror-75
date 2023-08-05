from autograd.tensor import Tensor
import numpy as np

"""
to quick new a tensor with requires grad 
also,
optimize for module
"""


class Parameter(Tensor):
    def __init__(self, *shape):
        data = np.random.randn(*shape)
        super(Parameter, self).__init__(data, requires_grad=True)
