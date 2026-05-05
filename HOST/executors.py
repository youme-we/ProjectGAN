import asyncio
import importlib
import os
import sys
import traceback

import requests
import torch
from colorama import Fore, Style

from utils import device


class Executor:
    def __init__(self):
        pass

    def listen(self, CONNECTION_STRING, __sio):
        self.CONNECTION_STRING = CONNECTION_STRING
        self.__sio = __sio

    def starter(self):
        project_name = "GAN1"  # input("Enter PROJECT_NAME: ")
        self.pull_project_config(project_name)
        self.load_inputs()
        self.load_targets()
        asyncio.create_task(self.reload_trainer())

    def load_inputs(self):
        self.inputs = torch.load(
            os.path.join(
                "./data", self.project_config["trainer"]["dataset"]["dir"], "inputs.pt"
            ),
            map_location=torch.device(device()),
            weights_only=False,
        )

    def load_targets(self):
        self.targets = torch.load(
            os.path.join(
                "./data", self.project_config["trainer"]["dataset"]["dir"], "targets.pt"
            ),
            map_location=torch.device(device()),
            weights_only=False,
        )

    def pull_project_config(self, project_name):
        res = requests.post(
            f"{self.CONNECTION_STRING}/read_project_config",
            json={"name": project_name},
        )
        self.project_config = res.json()

    async def toggle_pause_trainer(self):
        self._trainer.pause = not self._trainer.pause

    async def break_trainer(self):
        self._trainer.quit = True

    async def reload_trainer(self):
        try:
            if "trainers.trainer1" not in sys.modules:
                import trainers.trainer1

                trainers = trainers.trainer1
            else:
                trainers = importlib.reload(sys.modules["trainers.trainer1"])

            trainers.reload_submodules()
            self._trainer = trainers.Trainer(
                self.project_config["trainer"], self.inputs, self.targets
            )
            await self._trainer.listen(self.__sio)
            await self._trainer.train()
        except BaseException as e:
            print(Fore.RED + "\nERROR:", traceback.format_exc())
        print(
            Fore.YELLOW + "[ INFO ]:",
            "Press r or save the script to rerun — press z to exit",
        )
        print(
            Fore.GREEN
            + "---------------------------------------------------------\n\n"
            + Style.RESET_ALL
        )
