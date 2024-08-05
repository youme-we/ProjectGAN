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

def checking_data_actuality(Dataset, overview):
    input_shape = Dataset[0][0].shape[0]
    output_shape = torch.flatten(Dataset[0][1]).shape[0]
    if input_shape != overview.data.input_shape or output_shape != overview.data.output_shape1*overview.data.output_shape2*3:
        print(Fore.RED)
        print("Warning!: NN does not run with the latest data format")
        print(Style.RESET_ALL)
 
