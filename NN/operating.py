import requests
import asyncio
import socketio
sio = socketio.AsyncSimpleClient()
import json



class Operating():

    def __init__(self):
        self.URL = "http://localhost:3001/play_pause_save_py"
        self.play = True
        self.save = False

    async def play_pause_save(self, SOCKET_CONNECTION):
        while True:
            event = await SOCKET_CONNECTION.receive()
            print("here we go", event)
            self.play = event[1]["play"]
            self.save =  event[1]["save"]
