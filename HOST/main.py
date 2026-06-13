import asyncio
import os

import httpx
import socketio

import eventhandlers as eventhandlers
import executors as executors


class Host1:
    def __init__(self):
        self.__executor = executors.Executor()
        self.__eventhandler = eventhandlers.EventHandler(self.__executor)

    async def listen(self, CONNECTION_STRING):
        self.__http_client = httpx.AsyncClient(base_url=f"{CONNECTION_STRING}/")
        self.__socket_client = socketio.AsyncSimpleClient()
        await self.__socket_client.connect(CONNECTION_STRING)
        await self.__executor.listen(self.__http_client, self.__socket_client)
        await self.__executor.starter()
        await self.__eventhandler.listen(self.__http_client, self.__socket_client)
        await self.shutdown()

    async def shutdown(self):
        await self.__socket_client.disconnect()


if __name__ == "__main__":
    __host = Host1()
    asyncio.run(
        __host.listen(
            f"http://{os.getenv("HOST_SERVER", "localhost")}:{os.getenv("PORT_SERVER", 3001)}"
        )
    )
