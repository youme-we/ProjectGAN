import json
import requests
import asyncio
from colorama import Fore, Back, Style
import socketio
sio = socketio.AsyncSimpleClient()


class Operator():

    def __init__(self):
        self.URL = "http://localhost:3001/play_pause_save_py"
        self.play = True
        self.save = False

    async def play_pause_save(self, SOCKET_CONNECTION):
        while True:
            event = await SOCKET_CONNECTION.receive()
            # the event is structured as follows: list["origin", "message(json)"]
            if event[0] == "/play_pause_save_py":
                self.play = event[1]["play"]
                self.save = event[1]["save"]
                if self.play == False:
                    print(Fore.GREEN+"the calculation was paused")
                    print(Style.RESET_ALL)

    async def listen(self, SOCKET_CONNECTION):
        # makes listening to and receiving from sockets asynchronous
        asyncio.create_task(
            self.play_pause_save(SOCKET_CONNECTION))

    async def operate(self):
        # gives the Progmram "time" to empty the stack and clear/execute the event loop
        await asyncio.sleep(0)
        while self.play == False:
            # pauses the program while listening to the socket in parellel
            await asyncio.sleep(0)
            # program continues when Operator.play is set to True
