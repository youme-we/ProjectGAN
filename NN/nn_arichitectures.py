import torch
from torch import imag, nn, softmax
import numpy
from matplotlib import pyplot as plt
from subfunc import device


class GAN(nn.Module):
    def __init__(self, hyperparameters):
        for key, value in vars(hyperparameters).item():
            setatter(self, key, value)
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(input_shape, 1024),
            nn.Tanh(),
            nn.Linear(1024, 1024),
            nn.Tanh(),
            nn.Linear(
                1024, output_shape1 * output_shape2 * 3
            ),
            nn.Tanh(),
        )

        optimizer = torch.optim.SGD(
            self.model.parameters(),
            lr=self.learning_rate,
            momentum=self.momentum,
        )
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=1, gamma=0.9)
        samplers_data = sampler.SubsetRandomSampler(
            indices=torch.arange(self.N_samples)
        )
        training_dataloader = DataLoader(
            self.Dataset,
            sampler=samplers_data,
            batch_size=self.batch_size,
        )

    def forward(self, x):
        logits = self.linear_relu_stack(x)
        return logits

    def iter(self, X, y, loss_fn, optimizer, scheduler):
        self.train()  # prepers the model for training. sets all states like drop out... but doesn't train
        X, y = X, y
        y = self.flatten(y)
        # Compute prediction error

        pred = self.forward(X)
        loss = loss_fn(pred, y)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        # scheduler.step()

        self.pred = pred
        self.lable = y
        self.loss = loss.item()
