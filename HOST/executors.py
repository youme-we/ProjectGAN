import importlib
import requests
import sys
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
        self.pull_project_config()
        self.load_inputs()
        self.load_targets()
        await self.reload_Trainer()

    def load_inputs(self):
        self.inputs = torch.load(
            os.path.join(
                "./data", self.__project_config["metadata"]["data"], "inputs.pt"
            ),
            map_location=torch.device(device()),
            weights_only=False,
        )

    def load_targets(self):
        self.targets = torch.load(
            os.path.join(
                "./data", self.__project_config["metadata"]["data"], "targets.pt"
            ),
            map_location=torch.device(device()),
            weights_only=False,
        )

    def pull_project_config(self):
        res = requests.post(
            f"{self.CONNECTION_STRING}/read_project_config",
            json={"prj_name": self.PROJECT_NAME},
        )
        self.__project_config = res.json()

    async def reload_Trainer(self):
        try:
            if "Trainer.trainers" not in sys.modules:
                import Trainer.trainers

                trainers = Trainer.trainers
            else:
                trainers = importlib.reload(sys.modules["Trainer.trainers"])

            trainers.reload_submodules()
            __trainer = trainers.Trainer1(
                self.__project_config, self.inputs, self.targets
            )
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
