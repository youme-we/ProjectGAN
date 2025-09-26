import os
import socketio
import asyncio
import torch
import requests
import traceback
from importlib import reload
from colorama import Back, Fore, Style
import dev_utils
from utils import device
import executors as executors
import eventhandlers as eventhandlers


class Host:
    def __init__(self, PROJECT_NAME):
        self.PROJECT_NAME = PROJECT_NAME
        self.__sio = socketio.AsyncSimpleClient()
        self.__executor = executors.Executor1(self.PROJECT_NAME)
        self.__eventhandler = eventhandlers.EventHandler1(self.__executor)

    async def listen(self, CONNECTION_STRING):
        await self.__sio.connect(CONNECTION_STRING)
        await self.__executor.listen(CONNECTION_STRING, self.__sio)
        await self.__executor.starter()
        await self.__eventhandler.listen(CONNECTION_STRING, self.__sio)


if __name__ == "__main__":
    Host1 = Host(os.getenv("PROJECT_NAME"))
    asyncio.run(
        Host1.listen(
            f"http://{os.getenv("HOST_SERVER", "localhost")}:{os.getenv("PORT_SERVER", 3001)}"
        )
    )
