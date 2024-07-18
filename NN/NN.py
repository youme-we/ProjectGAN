import torch
from torch import imag, nn, softmax
import numpy
from matplotlib import pyplot as plt
from subfunc import device


class NeuralNetwork(nn.Module):
    def __init__(self, input_shape, output_shape):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(input_shape, 1024),
            nn.Tanh(),
            nn.Linear(1024, 1024),
            nn.Tanh(),
            nn.Linear(1024, output_shape),
            nn.LeakyReLU(0.9)
        )

    def forward(self, x):
        logits = self.linear_relu_stack(x)
        return logits

    def iter(self, X, y, model, loss_fn, optimizer, scheduler):
        model.train()  # prepers the model for training. sets all states like drop out... but doesn't train
        X, y = X, y
        y = self.flatten(y)
        # Compute prediction error

        pred = model(X)
        loss = loss_fn(pred, y)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        #scheduler.step()

        self.lable = y
        self.pred = pred
        self.loss = loss
