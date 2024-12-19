from typing import overload

import socketio
import torch
from torch import func, nn, optim
from torch.utils.data import DataLoader, sampler
from tqdm import tqdm

from Dataset import Dataset
from nn_architectures import GAN
from operating import Operator
from plotting2 import Plotters
from utils import checking_data_actuality, device, load_json

sio = socketio.AsyncSimpleClient()
torch.set_default_device(device())


class Trainer:
    def __init__(self, data):
        overview = load_json("../overview.json")
        for key, value in vars(overview.trainer).items():
            setattr(self, key, value)
        self.dataset = Dataset(data, overview.metadata)
        self.model = GAN(overview.hyperparameters, self.dataset)
        self.__plotter = Plotters(overview.plots)
        self.__operator = Operator(self.update_overview)

    async def init(self):
        await sio.connect("http://localhost:3001")
        SOCKET_CONNECTION = sio
        await self.__operator.listen(SOCKET_CONNECTION)
        await self.__plotter.listen(SOCKET_CONNECTION)

    def update_overview(self, new_overview):
        self.dataset.__update__(new_overview.metadata)
        self.model.__update__(new_overview.hyperparameters)

    async def train(self):
        for epoch in tqdm(range(self.epochs)):
            self.model.iter()
            await self.__operator.operate()
            if not self.__operator.run:
                self.__operator.group.cancel()
                return

            await self.__plotter.plot(epoch, self.model)
