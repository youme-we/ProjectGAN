import numpy
import torch
from matplotlib import pyplot as plt
from torch import imag, nn, softmax
from torch.utils.data import DataLoader, sampler
from utils import device


class GAN(nn.Module):
    def __init__(self, hyperparameters, dataset, input_transformer, target_transfomer):
        super().__init__()
        self.flatten = nn.Flatten()
        self.input_transformer = input_transformer
        self.target_transfomer = target_transfomer
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(dataset.input_shape, 1024),
            nn.ReLU(),
            nn.Linear(1024, 1024),
            nn.ReLU(),
            nn.Linear(1024, 2048),
            nn.ReLU(),
            nn.Linear(2048, dataset.output_shape1 * dataset.output_shape2 * 3),
            nn.Tanh(),
        )

        self.__update__(hyperparameters, dataset)

    def __update__(self, hyperparameters, dataset):
        self.__dict__.update(hyperparameters)
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
        self.train()
        for batch, (input, target) in enumerate(self.training_dataloader):
            X = self.input_transformer.normalize(input)
            y = self.target_transfomer.normalize(target)
            y = self.flatten(y)

            pred = self.forward(X)
            loss = self.loss_fn(pred, y)

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            # scheduler.step()

            self.pred = pred
            self.lable = y
            self.loss = loss.item()

    def predict(self, input):
        self.eval()
        X = self.input_transformer.normalize(input)
        pred = self.forward(X)
        return self.target_transfomer.denormalize(pred).int()
