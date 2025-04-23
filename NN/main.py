import torch
import asyncio
from Dataset import Dataset
from DataTransformer import DataTransformer
from nn_architectures import GAN
from operating import Operator
from plotting import Plotters
from tqdm import tqdm
from utils import device, load_json

torch.set_default_device(device())


class Trainer:
    def __init__(self, inputs, targets):
        overview = load_json("./overview.json")
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

    async def init(self, SOCKET_CONNECTION):
        await self.__operator.listen(SOCKET_CONNECTION)
        await self.__plotter.listen(SOCKET_CONNECTION)

    def update_overview(self, new_overview):
        # self.dataset.__update__(new_overview.metadata)
        self.model.__update__(new_overview.hyperparameters, self.dataset)

    async def train(self):
        for epoch in tqdm(range(1, self.epochs)):
            self.model.iter()
            await self.__operator.operate()
            if not self.__operator.run:
                await self.__operator.close()
                return

            await self.__plotter.plot(epoch, self.model, self.dataset)
