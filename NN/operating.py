import asyncio
import json
from types import SimpleNamespace
from colorama import Fore
import socketio

from utils import KeyPoller

sio = socketio.AsyncSimpleClient()


class Operator:
    def __init__(self, update_overview):
        self.update_overview = update_overview
        self.pause = False
        self.save = False
        self.run = True

    async def listen(self, SOCKET_CONNECTION):
        task1 = asyncio.create_task(self.on_GUI_handler(SOCKET_CONNECTION))
        task2 = asyncio.create_task(self.on_terminal_handler())
        self.group = asyncio.gather(task1, task2)

    async def operate(self):
        await asyncio.sleep(0.1)
        while self.pause:
            await asyncio.sleep(0)

    async def close(self):
        self.group.cancel()
        try:
            await self.group
        except asyncio.CancelledError:
            pass

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
        self.update_overview(
            json.loads(event[1]["overview"], object_hook=lambda d: SimpleNamespace(**d))
        )

    async def on_terminal_handler(self):
        with KeyPoller() as keyPoller:
            while True:
                await asyncio.sleep(0.01)
                key = keyPoller.poll()
                if key:
                    if key == "b":
                        self.run = False
                        self.pause = False
                    if key == "p":
                        self.pause = not self.pause
                        if self.pause:
                            print(
                                "\n[ Info ] The calculation was paused — press p to continue"
                            )
