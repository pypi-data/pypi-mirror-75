from autograd import Tensor, Parameter, Module


class Linear(Module):
    def __init__(self, in_size: int = 100, hidden_size: int = 50) -> None:
        self.w1 = Parameter(in_size, hidden_size)
        self.b1 = Parameter(hidden_size)

    def __call__(self, inputs: Tensor) -> Tensor:
        return self.predict(inputs)

    def predict(self, inputs: Tensor) -> Tensor:
        # inputs (batch_size,10)
        x1 = inputs @ self.w1 + self.b1  # (batch_size,num_hidden)

        return x1
