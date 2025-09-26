import requests
from colorama import Back, Fore, Style
import torch
import os
import traceback
from utils import device


class Executor1:
    def __init__(self, PROJECT_NAME):
        self.PROJECT_NAME = PROJECT_NAME

    async def listen(self, CONNECTION_STRING, __sio):
        self.CONNECTION_STRING = CONNECTION_STRING
        self.__sio = __sio

    async def starter(self):
        self.pull_overview()
        self.load_inputs()
        self.load_targets()
        await self.reload_Trainer()

    def load_inputs(self):
        self.inputs = torch.load(
            os.path.join("./data", self.__overview["metadata"]["data"], "inputs.pt"),
            map_location=torch.device(device()),
            weights_only=False,
        )

    def load_targets(self):
        self.targets = torch.load(
            os.path.join("./data", self.__overview["metadata"]["data"], "targets.pt"),
            map_location=torch.device(device()),
            weights_only=False,
        )

    def pull_overview(self):
        res = requests.post(
            f"{self.CONNECTION_STRING}/read_prj_overview",
            json={"prj_name": self.PROJECT_NAME},
        )
        self.__overview = res.json()

    async def reload_Trainer(self):
        try:
            if "trainer" not in locals():
                import Trainer.trainers as trainers
            else:
                trainers.reload_submodules()
                reload(trainers)
            __trainer = trainers.Trainer1(self.__overview, self.inputs, self.targets)
            await __trainer.listen(self.__sio)
            await __trainer.train()
        except BaseException as e:
            print(Fore.RED + "\nERROR:", traceback.format_exc())
        print(
            Fore.YELLOW + "[ INFO ]:",
            "Press r or save the script to rerun — press z to exit",
        )
        print(
            Fore.GREEN + "---------------------------------------------------------\n\n"
        )
