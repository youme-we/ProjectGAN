from importlib import reload
import torch
from tqdm import tqdm
import requests
import Trainer.datasets as datasets
import Trainer.models as models
import Trainer.plotting as plotting
import Trainer.operating as operating
import Trainer.data_transformers as data_transformers
from utils import device, load_json

torch.set_default_device(device())


def reload_submodules():
    reload(datasets)
    reload(models)
    reload(plotting)
    reload(operating)
    reload(data_transformers)


class Trainer:
    def __init__(self, __overview, inputs, targets):
        input_transformer = data_transformers.DataTransformer1(inputs)
        target_transfomer = data_transformers.DataTransformer1(targets)
        self.dataset = datasets.Dataset1(__overview["metadata"], inputs, targets)
        self.model = models.GAN1(
            __overview["hyperparameters"],
            self.dataset,
            input_transformer,
            target_transfomer,
        )
        self.__plotter = plotting.Plotter1(__overview["plot_rates"])
        self.__operator = operating.Operator1(self.__update__)
        self.__dict__.update(__overview["trainer"])

    def __update__(self, __overview):
        self.__dict__.update(__overview["trainer"])
        self.dataset.__update__(__overview["metadata"])
        self.model.__update__(__overview["hyperparameters"], self.dataset)
        self.__plotter.__update__(__overview["plot_rates"])

    async def listen(self, SOCKET_CONNECTION):
        await self.__operator.listen(SOCKET_CONNECTION)
        await self.__plotter.listen(SOCKET_CONNECTION)

    async def train(self):
        for epoch in tqdm(range(1, self.epochs)):
            self.model.iter()
            await self.__operator.operate()
            if not self.__operator.run:
                await self.__operator.close()
                return

            await self.__plotter.plot(epoch, self.model, self.dataset)
