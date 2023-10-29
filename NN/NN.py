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
            nn.Linear(input_shape, 128),
            nn.LeakyReLU(0.1),
            nn.Linear(128, 128),
            nn.LeakyReLU(0.1),
            nn.Linear(128, output_shape),
            nn.LeakyReLU(0.1)
        )

    def forward(self, x):
        #x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

    def iter(self, dataloader, model, loss_fn, optimizer, epoch, show_information_rate):
        model.train()  # prepers the model for training. sets all states like drop out... but doesn't train
        for batch, (X, y) in enumerate(dataloader):
            X, y = X.to(device()), y.to(device())
            y = self.flatten(y)
            # Compute prediction error
            pred = model(X)
            loss = loss_fn(pred, y)
            self.lable = y
            self.pred = pred
            self.loss = loss

            # Backpropagation
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
