import asyncio
import os

import socketio

import eventhandlers as eventhandlers
import executors as executors


class Host1:
    def __init__(self):
        self.__sio = socketio.AsyncSimpleClient()
        self.__executor = executors.Executor()
        self.__eventhandler = eventhandlers.EventHandler(self.__executor)

    async def listen(self, CONNECTION_STRING):
        await self.__sio.connect(CONNECTION_STRING)
        self.__executor.listen(CONNECTION_STRING, self.__sio)
        self.__executor.starter()
        await self.__eventhandler.listen(CONNECTION_STRING, self.__sio)
        await self.shutdown()

    async def shutdown(self):
        await self.__sio.disconnect()


if __name__ == "__main__":
    __host = Host1()
    asyncio.run(
        __host.listen(
            f"http://{os.getenv("HOST_SERVER", "localhost")}:{os.getenv("PORT_SERVER", 3001)}"
        )
    )
