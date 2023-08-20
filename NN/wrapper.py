import torch
import os
import time
import json
import sys
from colorama import Fore, Back, Style
from types import SimpleNamespace
from watchdog.events import FileSystemEventHandler, LoggingEventHandler
from watchdog.observers import Observer
from importlib import reload
from importlib.machinery import SourceFileLoader
import main
from NN_subfunc import device


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
        # vars which should be reloaded after every run
        hyperparameters = Dataloader.load_hyperparmeters()
        ##########################

        # imports and runs the Main class --> NN function
        from main import Main
        Main = Main(Dataset, hyperparameters)
        Main.NN()

    except Exception as e:
        print(Fore.RED+"Error:")
        print(Style.RESET_ALL)
        print(e)

    print("save the script to rerun, CTRL-C to exit")
    print("  ")
    print("#######################################")
    print("  ")
    print("  ")
    Watcher.reset()

    while True:  # runs as long as the Observer observes a change in the defined directory
        mutated = Watcher.mutated
        if (mutated):
            break

    while True:  # runs as long as the File itself gets updated
        tracked_path = Watcher.tracked_path
        root, ext = os.path.splitext(tracked_path)
        if ext:
            break

    if ext == ".py":
        Filename = os.path.basename(os.path.normpath(root))
        sub = SourceFileLoader(Filename, tracked_path).load_module()
        reload(sub)  # reloads sub_module which was modified

    reload(main)  # reloads main_module
