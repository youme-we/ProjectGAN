import asyncio
from colorama import Fore
from utils import KeyPoller
import os


class Operator1:
    def __init__(self):
        self.rerun = False
        self.quit = False

    async def listen(self, SOCKET_CONNECTION):
        # task1 = asyncio.create_task(self.on_GUI_handler(SOCKET_CONNECTION))
        task2 = asyncio.create_task(self.on_terminal_handler())
        self.group = asyncio.gather(task2)

    async def operate(self):
        while not self.rerun:
            await asyncio.sleep(0.001)
        self.rerun = False

    async def close(self):
        self.group.cancel()
        try:
            await self.group
        except asyncio.CancelledError:
            pass

    # async def on_GUI_handler(self, SOCKET_CONNECTION):
    #     while True:
    #         event = await SOCKET_CONNECTION.receive()
    #         if event[0] == "/pps_nn":
    #             self.pps_handler(event)
    #         if event[0] == "/tune_nn":
    #             await self.overview_handler(event)

    async def on_terminal_handler(self):
        last_modified = os.path.getmtime("./Trainer")
        with KeyPoller() as keyPoller:
            while True:
                await asyncio.sleep(0.01)
                current_modified = os.path.getmtime("./Trainer")
                key = keyPoller.poll()
                if key == "z":
                    self.rerun = True
                    self.quit = True
                if key == "r":
                    self.rerun = True
                if last_modified != current_modified:
                    self.rerun = True
                    last_modified = current_modified

    # def print_processing_status(self):
    #     if self.pause:
    #         print(
    #             Fore.YELLOW + "\n[ INFO ]:",
    #             "The calculation was paused — press p to continue",
    #         )
