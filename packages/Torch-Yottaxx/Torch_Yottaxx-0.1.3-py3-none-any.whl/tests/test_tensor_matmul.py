import unittest
from autograd import Tensor
import numpy as np


class TestTensorMatMul(unittest.TestCase):
    def test_simple_mul(self):
        t1 = Tensor([[1, 2], [3, 4], [5, 6]], requires_grad=True)
        t2 = Tensor([[10], [20]], requires_grad=True)
        t3 = t1 @ t2
        assert t3.data.tolist() == [[50], [110], [170]]
        grad = Tensor([[-1], [-2], [-3]])
        t3.backward(grad)

        assert np.all(t1.grad.data == grad.data @ t2.data.T)
        assert np.all(t2.grad.data == t1.data.T @ grad.data )
