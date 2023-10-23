import torch
import os
import time
import json
import sys
import traceback
from colorama import Fore, Back, Style
from types import SimpleNamespace
from watchdog.events import FileSystemEventHandler, LoggingEventHandler
from watchdog.observers import Observer
from importlib import reload
from importlib.machinery import SourceFileLoader
from subfunc import device
i = 0
try:
    import main
    i = 1
except:
    pass

    


def print_error(e):
    print(Fore.RED+"Error:")
    print(Style.RESET_ALL)
    print(traceback.format_exc())


class Dataloader:
    def __init__(self):
        self.device = device()

    def load_Dataset(self):
        return torch.load('data/data.pt', map_location=torch.device(self.device))

    def load_hyperparmeters(self):
        with open("hyperparameters.json", "r") as hyperparameters_file:
            hyperparameters = json.load(
                hyperparameters_file, object_hook=lambda d: SimpleNamespace(**d))
            return hyperparameters

    def load_parameters(self):
        pass


Dataloader = Dataloader()


class Watcher(FileSystemEventHandler):
    def reset(self):
        self.mutated = False

    def on_modified(self, event):
        self.tracked_path = event.src_path
        self.mutated = True


Watcher = Watcher()

# implements the Observer
Observer = Observer()
Observer.schedule(Watcher, path='./', recursive=False)
Observer.start()

# vars which should be loaded only once
Dataset = Dataloader.load_Dataset()
###########################


while True:  # runs as long as you do not interrup
    try:
        try:
            # vars which should be reloaded after every run
            hyperparameters = Dataloader.load_hyperparmeters()
            ##########################

            # imports and runs the Main class --> NN function
            from main import Main
            Main = Main(Dataset, hyperparameters)
            Main.NN()
            print("test")

        except KeyboardInterrupt:
            pass

    except Exception as e:
        print("error at running NN()")
        print_error(e)

    print("save the script to rerun, CTRL-C to exit")
    print("  ")
    print(Fore.GREEN+"#######################################")
    print(Style.RESET_ALL)
    print("  ")
    print("  ")

    while True:
        Watcher.reset()
        while True:  # runs as long as the Observer observes a change in the defined directory
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
            elif ext == ".py": 
                if i == 0:
                    import main

                else:
                    reload(main)  # reloads main_module
                i = 1
                break

        except Exception as e:  
            print("error at reloading modules")
            print_error(e)
