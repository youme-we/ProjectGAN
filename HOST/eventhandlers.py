import asyncio
from colorama import Fore
from utils import KeyPoller
import os
from datetime import datetime


class EventHandler1:
    def __init__(self, executor):
        self.__executor = executor
        self.hosting = True

    async def listen(self, CONNECTION_STRING, __sio):
        self.CONNECTION_STRING = CONNECTION_STRING
        self.__sio = __sio
        async with asyncio.TaskGroup() as tg:
            # task1 = asyncio.create_task(self.on_GUI_handler())
            task2 = tg.create_task(self.on_CLI_handler())

    async def on_GUI_handler(self):
        while self.hosting:
            event = await self.__sio.receive()

    async def on_CLI_handler(self):
        last_modified = os.path.getmtime("./Trainer")
        with KeyPoller() as keyPoller:
            while self.hosting:
                current_modified = os.path.getmtime("./Trainer")
                key = keyPoller.poll()
                if key is not None:
                    if key == "r":
                        self.__executor.pull_project_config()
                        await self.__executor.reload_Trainer()
                    elif key == "z":
                        self.hosting = False
                elif last_modified != current_modified:
                    self.__executor.pull_project_config()
                    await self.__executor.reload_Trainer()
                    last_modified = os.path.getmtime("./Trainer")
                else:
                    await asyncio.sleep(0)
