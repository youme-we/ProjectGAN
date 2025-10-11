from importlib import reload
import torch
import asyncio
from tqdm import tqdm
import requests
import Trainer.datasets as datasets
import Trainer.models as models
import Trainer.plotters as plotters
import Trainer.eventhandlers as eventhandlers
import Trainer.datatransformers as datatransformers
from utils import device, load_json
from colorama import Fore


torch.set_default_device(device())


def reload_submodules():
    reload(datasets)
    reload(models)
    reload(plotters)
    reload(eventhandlers)
    reload(datatransformers)


class Trainer1:
    def __init__(self, __overview, inputs, targets):
        input_transformer = datatransformers.DataTransformer1(inputs)
        target_transfomer = datatransformers.DataTransformer1(targets)
        self.__dataset = datasets.Dataset1(__overview["metadata"], inputs, targets)
        self.__model = models.GAN1(
            __overview["hyperparameters"],
            self.__dataset,
            input_transformer,
            target_transfomer,
        )
        self.__plotter = plotters.Plotter1(__overview["plot_rates"])
        self.__eventhandler = eventhandlers.EventHandler1(self.__update__)
        self.__dict__.update(__overview["trainer"])

    def __update__(self, __overview):
        self.__dict__.update(__overview["trainer"])
        self.__dataset.__update__(__overview["metadata"])
        self.__model.__update__(__overview["hyperparameters"], self.__dataset)
        self.__plotter.__update__(__overview["plot_rates"])

    async def listen(self, SOCKET_CONNECTION):
        await self.__eventhandler.listen(SOCKET_CONNECTION)
        await self.__plotter.listen(SOCKET_CONNECTION)

    async def train(self):
        pbar = tqdm(range(1, self.epochs + 1), desc="Training", unit="Epoch")
        for epoch in pbar:
            self.__model.iter()
            await self.__plotter.plot(epoch, self.__model, self.__dataset)
            if self.__eventhandler.pause_trainer:
                pbar.colour = "yellow"
                pbar.refresh()
                while self.__eventhandler.pause_trainer:
                    await asyncio.sleep(0)
                pbar.colour = "white"
            elif self.__eventhandler.break_trainer:
                await self.__eventhandler.close()
                return
            else:
                await asyncio.sleep(0)
        await self.__eventhandler.close()
