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
import operating


class Host:
    def __init__(self):
        self.PROJECT_NAME = os.getenv("PROJECT_NAME")
        self.HOST_SERVER = os.getenv("HOST_SERVER", "localhost")
        self.PORT_SERVER = os.getenv("PORT_SERVER", 3001)
        __overview = self.pull_overview()
        self.inputs = torch.load(
            os.path.join("./data", __overview["metadata"]["data"], "inputs.pt"),
            map_location=torch.device(device()),
            weights_only=False,
        )

        self.targets = torch.load(
            os.path.join("./data", __overview["metadata"]["data"], "targets.pt"),
            map_location=torch.device(device()),
            weights_only=False,
        )

        self.__sio = socketio.AsyncSimpleClient()
        self.__operator = operating.Operator1()

    def pull_overview(self):
        res = requests.post(
            f"http://{self.HOST_SERVER}:{self.PORT_SERVER}/read_prj_overview",
            json={"prj_name": self.PROJECT_NAME},
        )
        return res.json()

    async def host(self):
        await self.__sio.connect(f"http://{self.HOST_SERVER}:{self.PORT_SERVER}")
        await self.__operator.listen(self.__sio)
        while True:
            __overview = self.pull_overview()
            try:
                if "trainer" not in locals():
                    import Trainer.trainer as trainer
                else:
                    reload(trainer)
                trainer.reload_submodules()
                self.trainer = trainer.Trainer(__overview, self.inputs, self.targets)
                await self.trainer.listen(self.__sio)
                # self.trainer.__update__(__overview)
                await self.trainer.train()
            except Exception as e:
                print(Fore.RED + "\nERROR:", traceback.format_exc())
            print(
                Fore.YELLOW + "[ INFO ]:",
                "Press r or save the script to rerun — press z to exit",
            )
            print(
                Fore.GREEN
                + "---------------------------------------------------------\n\n"
            )
            await self.__operator.operate()
            if self.__operator.quit:
                await self.__operator.close()
                return


if __name__ == "__main__":
    Host1 = Host()
    asyncio.run(Host1.host())
