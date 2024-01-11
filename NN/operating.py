import json
import requests
import asyncio
from colorama import Fore, Back, Style
import socketio
import keyboard
import sys
import select
from pynput.keyboard import Listener
from keyboard import KeyPoller
sio = socketio.AsyncSimpleClient()


class Operator():

    def __init__(self):
        self.URL = "http://localhost:3001/play_pause_save_py"
        self.pause = False
        self.save = False
        self.run = True

    async def play_pause_save(self, SOCKET_CONNECTION):
        while True:
            event = await SOCKET_CONNECTION.receive()
            # the event is structured as follows: list["origin", "message(json)"]
            if event[0] == "/play_pause_save_py":
                self.pause = event[1]["pause"]
                self.save = event[1]["save"]
                self.run = event[1]["run"]

            if self.pause == True:
                print(Fore.GREEN+"the calculation was paused")
                print(Style.RESET_ALL)

    async def keyboard(self):
        with KeyPoller() as keyPoller:
            while True:
                await asyncio.sleep(0)
                key = keyPoller.poll()
                if not key is None:
                    if key == "b":
                        self.run = False
                        #self.task2.cancel()
                        #self.task1.cancel()
                        self.group.cancel()
                

    async def listen(self, SOCKET_CONNECTION):
        # makes listening to and receiving from sockets asynchronous
        self.task1 = asyncio.create_task(
            self.play_pause_save(SOCKET_CONNECTION)
        )
        self.task2 = asyncio.create_task(
            self.keyboard()
        )
        self.group = asyncio.gather(self.task2, self.task1)

    async def operate(self):
        # gives the Progmram "time" to empty the stack and clear/execute the event loop
        await asyncio.sleep(0)
        while self.pause == True:
            # pauses the program while listening to the socket in parellel
            await asyncio.sleep(0)
            # program continues when Operator.play is set to True
