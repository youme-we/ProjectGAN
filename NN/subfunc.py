import torch
import json
from types import SimpleNamespace

def device():
    device = (
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
        if torch.backends.mps.is_available()
        else "cpu")

    return device


def load_json(file):
    with open(file, "r") as data_file:
        data = json.load(
            data_file, object_hook=lambda d: SimpleNamespace(**d))
    return data
