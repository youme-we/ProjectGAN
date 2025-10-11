import asyncio
from colorama import Fore
from utils import KeyPoller
import os
from datetime import datetime


class EventHandler1:
    def __init__(self, executor):
        self.__executor = executor

    async def listen(self, CONNECTION_STRING, __sio):
        self.CONNECTION_STRING = CONNECTION_STRING
        self.__sio = __sio
        # task1 = asyncio.create_task(self.on_GUI_handler())
        task2 = asyncio.create_task(self.on_CLI_handler())
        self.tasks = await asyncio.gather(task2)  # , task1)

    async def on_GUI_handler(self):
        while True:
            event = await self.__sio.receive()

    async def on_CLI_handler(self):
        last_modified = os.path.getmtime("./Trainer")
        with KeyPoller() as keyPoller:
            while True:
                current_modified = os.path.getmtime("./Trainer")
                key = keyPoller.poll()
                if key is not None:
                    if key == "r":
                        print(datetime.now())
                        self.__executor.pull_overview()
                        print(datetime.now())
                        await self.__executor.reload_Trainer()
                    elif key == "z":
                        return
                elif last_modified != current_modified:
                    self.__executor.pull_overview()
                    await self.__executor.reload_Trainer()
                    last_modified = os.path.getmtime("./Trainer")
                else:
                    await asyncio.sleep(0)
