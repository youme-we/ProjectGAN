import asyncio
from colorama import Fore, Back, Style
import socketio
from keyboard import KeyPoller
import json
from types import SimpleNamespace
sio = socketio.AsyncSimpleClient()


class Operator():

    def __init__(self, props):
        self.props = props
        self.pause = False
        self.save = False
        self.run = True

    async def listen(self, SOCKET_CONNECTION):
        task1 = asyncio.create_task(
            self.on_GUI_handler(SOCKET_CONNECTION)
        )
        task2 = asyncio.create_task(
            self.on_terminal_handler()
        )

        self.group = asyncio.gather(task1, task2)

    async def operate(self):
        await asyncio.sleep(0.1)
        while self.pause:
            await asyncio.sleep(0)

    async def on_GUI_handler(self, SOCKET_CONNECTION):
        while True:
            event = await SOCKET_CONNECTION.receive()
            if event[0] == "/pps_nn":
                self.pps_handler(event)
            if event[0] == "/tune_nn":
                await self.overview_handler(event)

    def pps_handler(self, event):
        self.pause = event[1]["pause"]
        self.save = event[1]["save"]
        self.run = event[1]["run"]
        self.print_processing_status()

    async def overview_handler(self, event):
        self.props.overview = json.loads(
            event[1]["overview"], object_hook=lambda d: SimpleNamespace(**d)).overview

    async def on_terminal_handler(self):
        with KeyPoller() as keyPoller:
            while True:
                await asyncio.sleep(0)
                key = keyPoller.poll()
                if not key is None:
                    if key == "b":
                        self.run = False
                        self.pause = False
                    if key == "p":
                        self.pause = not self.pause
                        self.print_processing_status()

    def print_processing_status(self):
        if self.pause:
            print(Fore.GREEN+"The calculation was paused")
            print(Style.RESET_ALL)

        if not self.run:
            print(Fore.GREEN+"The calculation was ended & the weights were saved")
            print(Style.RESET_ALL)
