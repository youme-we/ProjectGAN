import numpy
import torch
from matplotlib import pyplot as plt
from torch import imag, nn, softmax
from torch.utils.data import DataLoader, sampler

from utils import device


class GAN(nn.Module):
    def __init__(self, hyperparameters, dataset):
        for key, value in vars(hyperparameters).items():
            setattr(self, key, value)
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(dataset.input_shape, 1024),
            nn.Tanh(),
            nn.Linear(1024, 1024),
            nn.Tanh(),
            nn.Linear(1024, dataset.output_shape1 * dataset.output_shape2 * 3),
            nn.Tanh(),
        )

        self.samplers_data = sampler.SubsetRandomSampler(
            indices=torch.arange(self.n_samples)
        )
        self.training_dataloader = DataLoader(
            dataset,
            sampler=self.samplers_data,
            batch_size=self.batch_size,
        )

        self.optimizer = torch.optim.SGD(
            self.parameters(),
            lr=self.learning_rate,
            momentum=self.momentum,
        )
        self.scheduler = torch.optim.lr_scheduler.StepLR(
            self.optimizer, step_size=1, gamma=0.9
        )

        self.loss_fn = nn.MSELoss()

    def forward(self, x):
        logits = self.linear_relu_stack(x)
        return logits

    def iter(self):
        for batch, (X, y) in enumerate(self.training_dataloader):
            self.train()  # prepers the model for training. sets all states like drop out... but doesn't train
            y = self.flatten(y)
            # Compute prediction error

            pred = self.forward(X)
            loss = self.loss_fn(pred, y)

            # Backpropagation
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            # scheduler.step()

            self.pred = pred
            self.lable = y
            self.loss = loss.item()
