import asyncio
import json
from types import SimpleNamespace
from colorama import Fore
from numpy import trace
from utils import KeyPoller
import traceback


class EventHandler1:
    def __init__(self, update_trainer):
        self.update_trainer = update_trainer
        self.pause_trainer = False
        self.break_trainer = False
        self.save = False

    async def listen(self, SOCKET_CONNECTION):
        task1 = asyncio.create_task(self.on_GUI_handler(SOCKET_CONNECTION))
        task2 = asyncio.create_task(self.on_terminal_handler())


    async def on_GUI_handler(self, SOCKET_CONNECTION):
        while not self.break_trainer:
            event = await SOCKET_CONNECTION.receive()
            if event[0] == "/pps_nn":
                self.pause_trainer = event[1]["pause_trainer"]
                self.save_trainer = event[1]["save_trainer"]
                self.break_trainer = event[1]["break_trainer"]
            if event[0] == "/tune_nn":
                await self.overview_handler(event)

    async def on_terminal_handler(self):
        with KeyPoller() as keyPoller:
            while not self.break_trainer:
                key = keyPoller.poll()
                if key is not None:
                    if key == "p":
                        self.pause_trainer = not self.pause_trainer
                    elif key == "b":
                        self.break_trainer = True
                else:
                    await asyncio.sleep(0)

    async def overview_handler(self, event):
        self.update_trainer(json.loads(event[1]["overview"]))
