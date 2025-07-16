import torch
import asyncio
from tqdm import tqdm
import requests
import os
from datasets import Dataset1
from data_transformers import DataTransformer1
from models import GAN1
from operating import Operator
from plotting import Plotters
from utils import device, load_json
import numpy as np

torch.set_default_device(device())


class Trainer:
    def __init__(self, overview, inputs, targets):
        self.__dict__.update(overview["trainer"])
        input_transformer = DataTransformer1(inputs)
        target_transfomer = DataTransformer1(targets)
        self.dataset = Dataset1(overview["metadata"], inputs, targets)
        self.model = GAN1(
            overview["hyperparameters"],
            self.dataset,
            input_transformer,
            target_transfomer,
        )
        self.__plotter = Plotters(overview["plot_rates"])
        self.__operator = Operator(self.update_overview)

    async def init(self, SOCKET_CONNECTION):
        await self.__operator.listen(SOCKET_CONNECTION)
        await self.__plotter.listen(SOCKET_CONNECTION)

    def update_overview(self, new_overview):
        self.dataset.__update__(new_overview["metadata"])
        self.model.__update__(new_overview["hyperparameters"], self.dataset)

    async def train(self):
        for epoch in tqdm(range(1, self.epochs)):
            self.model.iter()
            await self.__operator.operate()
            if not self.__operator.run:
                await self.__operator.close()
                return

            await self.__plotter.plot(epoch, self.model, self.dataset)
