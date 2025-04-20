import asyncio
import os
from importlib import reload
from importlib.machinery import SourceFileLoader

import torch
from colorama import Back, Fore, Style
from watchdog.events import FileSystemEventHandler, LoggingEventHandler
from watchdog.observers import Observer

import devel_utils
from utils import device, load_json
import readchar

overview = load_json("./overview.json")


import socketio

sio = socketio.AsyncSimpleClient()


class Watcher(FileSystemEventHandler):
    def reset(self):
        self.mutated = False

    def on_modified(self, event):
        self.tracked_path = event.src_path
        self.mutated = True


Watcher = Watcher()

# implements the Observer
Observer = Observer()  # external libaray
Observer.schedule(Watcher, path="./", recursive=False)
Observer.start()

# vars which should be loaded only once
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


async def wrapper():
    i = 0
    try:
        import main

        i = 1
    except:
        pass

    while True:  # runs as long as you do not InterruptedError
        try:
            # vars which should be reloaded after every run
            ##########################

            # imports and runs the Main class --> NN function
            from main import Trainer

            Trainer = Trainer(inputs, labels)
            PORT_SERVER = os.getenv("PORT_SERVER", 3001)
            await sio.connect(f"http://server:{PORT_SERVER}")
            await Trainer.init(sio)
            await Trainer.train()

        except Exception as e:
            diagnostics(e, "error")
            diagnostics("error at runtime", "wrapper_info")

        print("save the script to rerun, or press Ctrl-z to exit\n")
        print(Fore.GREEN + "#################################################\n\n")

        while True:
            Watcher.reset()
            while True:
                if readchar.readchar() == "\x1a":
                    await sio.disconnect()
                    return
                # runs as long as the Observer observes a change in the defined directory
                mutated = Watcher.mutated
                if mutated:
                    break

            while True:  # runs as long as the File itself gets updated
                tracked_path = Watcher.tracked_path
                root, ext = os.path.splitext(tracked_path)
                if ext:
                    break
            try:
                if ext == ".py" and root != "/Users/skost/coding-s/ProjectGAN/NN/main":
                    Filename = os.path.basename(os.path.normpath(root))
                    sub = SourceFileLoader(Filename, tracked_path).load_module()
                    reload(sub)  # reloads sub_module which was Modified
                    if i == 0:
                        import main

                    else:
                        reload(main)  # reloads main_module
                    i = 1
                    break
                elif ext == ".py" or ".json":
                    if i == 0:
                        import main

                    else:
                        reload(main)  # reloads main_module
                    i = 1
                    break

            except Exception as e:
                diagnostics(e, "error")
                diagnostics("error at reloading modules", "wrapper_info")


asyncio.run(wrapper())
