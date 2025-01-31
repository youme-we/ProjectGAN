from asyncio import DatagramTransport

import socketio
import torch
from tqdm import tqdm

from Dataset import Dataset
from DataTransformer import DataTransformer
from nn_architectures import GAN
from operating import Operator
from plotting import Plotters
from utils import device, load_json

sio = socketio.AsyncSimpleClient()
torch.set_default_device(device())


class Trainer:
    def __init__(self, inputs, targets):
        overview = load_json("../overview.json")
        for key, value in vars(overview.trainer).items():
            setattr(self, key, value)
        input_transformer = DataTransformer(inputs)
        target_transfomer = DataTransformer(targets)
        self.dataset = Dataset(overview.metadata, inputs, targets)
        self.model = GAN(
            overview.hyperparameters, self.dataset, input_transformer, target_transfomer
        )
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
        for epoch in tqdm(range(1, self.epochs)):
            self.model.iter()
            await self.__operator.operate()
            if not self.__operator.run:
                self.__operator.group.cancel()
                return

            await self.__plotter.plot(epoch, self.model, self.dataset)
