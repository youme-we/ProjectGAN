import json
import requests
import asyncio
from colorama import Fore, Back, Style
import socketio
sio = socketio.AsyncSimpleClient()


class Operating():

    def __init__(self):
        self.URL = "http://localhost:3001/play_pause_save_py"
        self.play = True
        self.save = False

    async def play_pause_save(self, SOCKET_CONNECTION):
        while True:
            event = await SOCKET_CONNECTION.receive()
            if event[0] == "/play_pause_save_py":
                self.play = event[1]["play"]
                self.save = event[1]["save"]
                if self.play == False:
                    print(Fore.GREEN+"the calculation was paused")
                    print(Style.RESET_ALL)
