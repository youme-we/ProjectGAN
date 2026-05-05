import torch
from torch import nn
from torch.utils.data import DataLoader, sampler


class Model(nn.Module):
    def __init__(self, model_config, input_shape, target_shape):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(input_shape, 512),
            nn.Tanh(),
            nn.Linear(512, 512),
            nn.Tanh(),
            nn.Linear(512, target_shape),
            nn.Tanh(),
        )

        self.__dict__.update(model_config)

    def __update__(self, model_config):
        self.__dict__.update(model_config)

    def forward(self, x):
        return self.linear_relu_stack(x)
