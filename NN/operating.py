import asyncio
from colorama import Fore, Back, Style
import socketio
from keyboard import KeyPoller
from subfunc import device, load_json
import json
from types import SimpleNamespace
sio = socketio.AsyncSimpleClient()


class Operator():

    def __init__(self, overview):
        self.pause = False
        self.save = False
        self.run = True
        self.overview  = overview
        

    async def pps_GUI(self, SOCKET_CONNECTION):
        while True:
            event = await SOCKET_CONNECTION.receive()
            # the event is structured as follows: list["origin", "message(json)"]
            if event[0] == "/pps_nn":
                self.pause = event[1]["pause"]
                self.save = event[1]["save"]
                self.run = event[1]["run"]
                await self.print_processing_status()
            if event[0] == "/tune_nn":
                data = event[1]["overview"]
                overview = json.loads(
                    data, object_hook=lambda d: SimpleNamespace(**d)).overview
                self.overview = overview

    async def pps_terminal(self):
        with KeyPoller() as keyPoller:
            while True:
                # is needed so that the rest of the programm gets time(the bigger that timeperiod, the rest of the program gets more time to be run) to be run
                await asyncio.sleep(0)
                key = keyPoller.poll()
                if not key is None:
                    if key == "b":
                        self.run = False
                        self.pause = False
                    if key == "p":
                        self.pause = not self.pause
                        await self.print_processing_status()

    async def print_processing_status(self):
        if self.pause:
            print(Fore.GREEN+"The calculation was paused")
            print(Style.RESET_ALL)

        if self.run == False:
            print(Fore.GREEN+"The calculation was ended & the weights were saved")
            print(Style.RESET_ALL)

    async def listen(self, SOCKET_CONNECTION):
        # makes listening to and receiving from sockets asynchronous
        self.task1 = asyncio.create_task(
            self.pps_GUI(SOCKET_CONNECTION)
        )
        self.task2 = asyncio.create_task(
            self.pps_terminal()
        )

        self.group = asyncio.gather(self.task2, self.task1)

    async def operate(self):
        # gives the Progmram "time" to empty the stack and clear/execute the event loop
        await asyncio.sleep(0.1)
        while self.pause:
            # pauses the program while listening to the socket in parellel
            await asyncio.sleep(0)
            # program continues when Operator.play is set to True
