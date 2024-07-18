import torch
import json
from types import SimpleNamespace
from colorama import Fore, Back, Style

def device():
    device = (
        "cuda"
        if torch.cuda.is_available()
        else "mps"
        if torch.backends.mps.is_available()
        else "cpu")

    return device


def load_json(file):
    with open(file, "r") as data_file:
        data = json.load(
            data_file, object_hook=lambda d: SimpleNamespace(**d))
    return data

def checking_data_actuality(input_shape, output_shape, data_p):
    if input_shape != data_p.input_shape or output_shape != data_p.shape_1*data_p.shape_2*3:
        print(Fore.RED)
        print("Warning!: NN does not run with the latest data format")
        print(Style.RESET_ALL)
 
