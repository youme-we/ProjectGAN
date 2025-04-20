import os
import torch
import asyncio
import socketio
from importlib import reload
from importlib.machinery import SourceFileLoader
from colorama import Back, Fore, Style
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from utils import device, load_json
import traceback
import dev_utils

sio = socketio.AsyncSimpleClient()
overview = load_json("./overview.json")


class Watcher(FileSystemEventHandler):
    def reset(self):
        self.mutated = False

    def on_modified(self, event):
        self.tracked_path = event.src_path
        self.mutated = True


Watcher = Watcher()

Observer = Observer()  # external libaray
Observer.schedule(Watcher, path="./", recursive=False)
Observer.start()


######### vars which should be loaded only once
inputs = torch.load(
    os.path.join(overview.metadata.folder_dir, "inputs.pt"),
    map_location=torch.device(device()),
    weights_only=False,
)

labels = torch.load(
    os.path.join(overview.metadata.folder_dir, "labels.pt"),
    map_location=torch.device(device()),
    weights_only=False,
)
#########


async def wrapper():
    PORT_SERVER = os.getenv("PORT_SERVER", 3001)
    await sio.connect(f"http://host.docker.internal:{PORT_SERVER}")
    i = 0
    try:
        import main

        i = 1
    except:
        pass

    while True:
        try:
            from main import Trainer

            Trainer = Trainer(inputs, labels)
            await Trainer.init(sio)
            await Trainer.train()

        except Exception as e:
            print(Fore.RED + "\nERROR:", traceback.format_exc())
        while True:
            print(
                Fore.YELLOW + "[ INFO ]:",
                "Save the script to rerun — press Ctrl+Z to exit",
            )
            print(
                Fore.GREEN
                + "---------------------------------------------------------\n\n"
            )

            Watcher.reset()
            while True:
                await asyncio.sleep(0)
                mutated = Watcher.mutated
                if mutated:
                    break

            while True:
                tracked_path = Watcher.tracked_path
                root, ext = os.path.splitext(tracked_path)
                if ext:
                    break
            try:
                if ext == ".py" and os.path.basename(root) != "main":
                    Filename = os.path.basename(os.path.normpath(root))
                    sub = SourceFileLoader(Filename, tracked_path).load_module()
                    reload(sub)
                    if i == 0:
                        import main

                    else:
                        reload(main)
                    i = 1
                    break
                elif ext == ".py" or ".json":
                    if i == 0:
                        import main

                    else:
                        reload(main)
                    i = 1
                    break

            except Exception as e:
                print(Fore.RED + "\nERROR:", traceback.format_exc())


asyncio.run(wrapper())
