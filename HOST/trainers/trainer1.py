import asyncio
from importlib import reload

import torch

# import Trainer.datatransformers as datatransformers
# import Trainer.eventhandlers as eventhandlers
# import Trainer.models as models
# import Trainer.plotters as plotters
from torch import nn
from torch.utils.data import DataLoader, sampler
from tqdm import tqdm

import datasets
import datatransformers
import models
import plotters
from utils import device

torch.set_default_device(device())


def reload_submodules():
    reload(datasets)
    reload(models)
    reload(plotters)
    reload(datatransformers)


class Trainer:
    def __init__(self, __trainer_config, inputs, targets):
        self.pause = False
        self.quit = False
        self.input_transformer = datatransformers.DataTransformer(inputs)
        self.target_transfomer = datatransformers.DataTransformer(targets)
        self._dataset = datasets.Dataset(__trainer_config["dataset"], inputs, targets)
        self._model = models.Model(
            __trainer_config["model"],
            self._dataset.input_dim,
            self._dataset.target_dim,
        )
        self._plotter = plotters.Plotter(__trainer_config["plotter"], self)
        self.__update__(__trainer_config)

    def __update__(self, __trainer_config):
        self.__dict__.update(__trainer_config)
        self.samplers_data = sampler.SubsetRandomSampler(
            indices=torch.arange(self.sample_size)
        )
        self.training_dataloader = DataLoader(
            self._dataset,
            sampler=self.samplers_data,
            batch_size=self.batch_size,
        )

        self.optimizer = torch.optim.SGD(
            self._model.parameters(),
            lr=self.learning_rate,
            momentum=self.momentum,
        )
        self.scheduler = torch.optim.lr_scheduler.StepLR(
            self.optimizer, step_size=1, gamma=0.9
        )

        self.loss_fn = nn.MSELoss()

        self._dataset.__update__(__trainer_config["dataset"])
        self._model.__update__(__trainer_config["model"])
        self._plotter.__update__(__trainer_config["plotter"])

    async def listen(self, SOCKET_CONNECTION):
        await self._plotter.listen(SOCKET_CONNECTION)

    def forward(self, latent_vector):
        return self._model.linear_relu_stack(latent_vector)

    def iter(self):
        self._model.train()
        for batch, (input, target) in enumerate(self.training_dataloader):
            X = self.input_transformer.normalize(input)
            y = self.target_transfomer.normalize(target)
            y = self._model.flatten(y)
            pred = self._model.forward(X)
            loss = self.loss_fn(pred, y)

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            # scheduler.step()

            self.pred = pred
            self.lable = y
            self.loss = loss.item()

    def predict(self, input):
        self._model.eval()
        X = self.input_transformer.normalize(input)
        pred = self.forward(X)
        return self.target_transfomer.denormalize(pred).int()

    async def train(self):
        pbar = tqdm(range(1, self.epochs + 1), desc="Training", unit="Epoch")
        for epoch in pbar:
            self.iter()
            await self._plotter.plot(epoch)
            if self.pause:
                pbar.colour = "yellow"
                pbar.refresh()
                while self.pause:
                    await asyncio.sleep(0)
                pbar.colour = "white"
            elif self.quit:
                return
            else:
                await asyncio.sleep(0)
