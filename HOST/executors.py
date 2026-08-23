import asyncio
import importlib
import os
import sys
import traceback

import httpx
import torch
from bson import ObjectId
from colorama import Fore, Style

from utils import device


class Executor:
    def __init__(self):
        pass

    async def listen(self, __http_client, __socket_client):
        self.__http_client = __http_client
        self.__socket_client = __socket_client

    async def starter(self):
        config_id = ObjectId("69f244289e1ba92747476ebf")  # input("Enter CONFIG_ID: ")
        await self.pull_config(str(config_id))
        self.load_inputs()
        self.load_targets()
        asyncio.create_task(self.reload_trainer())

    def load_inputs(self):
        self.inputs = torch.load(
            os.path.join(
                "./data", self.config["trainer"]["dataset"]["dir"], "inputs.pt"
            ),
            map_location=torch.device(device()),
        )

    def load_targets(self):
        self.targets = torch.load(
            os.path.join(
                "./data", self.config["trainer"]["dataset"]["dir"], "targets.pt"
            ),
            map_location=torch.device(device()),
        )

    async def pull_config(self, project_name):
        response = await self.__http_client.post(
            "read_project_config",
            json={"_id": project_name},
        )
        self.config = response.json()

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
                self.config["_id"], self.config["trainer"], self.inputs, self.targets
            )
            await self._trainer.listen(self.__socket_client)
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
