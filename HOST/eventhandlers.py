import asyncio
import os

from utils import KeyPoller, get_last_modified_time


class EventHandler:
    def __init__(self, executor):
        self.__executor = executor
        self.hosting = True

    async def listen(self, __http_client, __socket_client):
        self.__socket_client = __socket_client
        async with asyncio.TaskGroup() as tg:
            # task1 = asyncio.create_task(self.on_GUI_handler())
            task2 = tg.create_task(self.on_CLI_handler())

    async def on_GUI_handler(self):
        while self.hosting:
            event = await self.__socket_client.receive()

    async def on_CLI_handler(self):
        last_modified = get_last_modified_time()
        with KeyPoller() as keyPoller:
            while self.hosting:
                current_modified = get_last_modified_time()
                key = keyPoller.poll()
                if key is not None:
                    if key == "r":
                        asyncio.create_task(self.__executor.pull_project_config("GAN1"))
                        asyncio.create_task(self.__executor.reload_trainer())
                    elif key == "z":
                        self.hosting = False
                    elif key == "p":
                        asyncio.create_task(self.__executor.toggle_pause_trainer())
                    elif key == "b":
                        asyncio.create_task(self.__executor.break_trainer())
                elif last_modified != current_modified:
                    print("modified")
                    asyncio.create_task(self.__executor.pull_project_config("GAN1"))
                    asyncio.create_task(self.__executor.reload_trainer())
                    last_modified = get_last_modified_time()
                else:
                    await asyncio.sleep(0)
