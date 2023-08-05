from autograd import Tensor, Parameter, Module
from autograd.Layers import Linear
import numpy as np


class SimpleAttention(Module):
    def __init__(self, in_size: int = 100) -> None:
        self.size = in_size

    def __call__(self, q, k, v):
        return self.predict(q, k, v)

    def predict(self, q: Tensor, k: Tensor, v: Tensor) -> Tensor:
        # q,k,v (batch_size,,length,size)
        # q*k -> (batch_size,head,length,length)
        # q*k*v->(batch_size,head,length,size)
        attn = q @ k.transpose((-1,-2))
        output = attn @ v
        return output
