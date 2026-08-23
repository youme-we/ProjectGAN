import asyncio
from importlib import reload

import torch
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
    def __init__(self, config_id, trainer_config, inputs, targets):
        self.pause = False
        self.quit = False
        print(config_id)
        self.__dict__.update(trainer_config)
        self.imagetransformer = datatransformers.ImageTransformer()
        self.input_normalizer = datatransformers.Normalizer(inputs)
        self.target_normalizer = datatransformers.Normalizer(targets)
        self.training_dataset = datasets.Dataset(
            trainer_config["dataset"],
            inputs[: self.sample_size],
            targets[: self.sample_size],
        )
        self.testing_dataset = datasets.Dataset(
            trainer_config["dataset"],
            inputs[self.sample_size :],
            targets[self.sample_size :],
        )
        self.training_sampler = sampler.SubsetRandomSampler(
            indices=torch.arange(self.sample_size)
        )
        self._model = models.Model(
            trainer_config["model"],
            self.training_dataset.latent_dim,
            self.training_dataset.target_dim,
        )

        self.loss_fn = nn.MSELoss()
        self._plotter = plotters.Plotter(trainer_config["plotter"])

        self.__update__(trainer_config)

    def __update__(self, trainer_config):
        self.__dict__.update(trainer_config)

        self.training_dataloader = DataLoader(
            self.training_dataset,
            sampler=self.training_sampler,
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

        self._plotter.__update__(trainer_config["plotter"])

    async def listen(self, SOCKET_CONNECTION):
        await self._plotter.listen(SOCKET_CONNECTION)

    def forward(self, latent_vector):
        return self._model.linear_relu_stack(latent_vector)

    def iter(self, dataloader):
        self._model.train()
        total_loss = 0
        for batch, (input, target) in enumerate(dataloader):
            X = self.input_normalizer.normalize(input)
            y = self.target_normalizer.normalize(target)
            y = self._model.flatten(y)
            pred = self._model.forward(X)
            loss = self.loss_fn(pred, y)
            total_loss += loss.item()

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            # scheduler.step()

        return {"loss": total_loss / (batch + 1)}

    def test(self, input, target):
        self._model.eval()
        X = self.input_normalizer.normalize(input)
        pred = self.forward(X)
        output = self.target_normalizer.denormalize(pred)
        b64 = self.imagetransformer.encode_images_to_base64(
            output,
            self.training_dataset.image_height_px,
            self.training_dataset.image_width_px,
        )
        return {"pred": pred, "output": output, "b64": b64}

    def predict(self, input):
        self._model.eval()
        X = self.input_normalizer.normalize(input)
        pred = self.forward(X)
        return {"output": self.target_normalizer.denormalize(pred)}

    async def train(self):
        pbar = tqdm(range(1, self.epochs + 1), desc="Training", unit="Epoch")
        for epoch in pbar:
            iter_result = self.iter(self.training_dataloader)
            train_result = self.test(
                self.training_dataset[0:2][0], self.training_dataset[0:2][1]
            )
            test_result = self.test(
                self.testing_dataset[0:2][0], self.testing_dataset[0:2][1]
            )
            await self._plotter.plot(epoch, iter_result, train_result, test_result)
            if self.pause:
                pbar.colour = "yellow"
                pbar.refresh()
                while self.pause:
                    await asyncio.sleep(0.5)
                pbar.colour = "white"
            elif self.quit:
                return
            else:
                await asyncio.sleep(0.5)
