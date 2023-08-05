import unittest
from autograd import Tensor

import numpy as np


class TestTensorTranspose(unittest.TestCase):
    def test_simple_add(self):
        t1 = Tensor(np.random.randn(3, 4, 5), requires_grad=True)
        t2 = t1.transpose((1, 2, 0))
        assert t2.data.shape == (4, 5, 3)
        t2.backward(Tensor(np.ones((4, 5, 3))))
        assert t1.grad.data.shape == (3, 4, 5)
