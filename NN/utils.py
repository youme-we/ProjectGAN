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
    input_shape_Dataset = Dataset[0][0].shape[0]
    input_shape_overview = overview.data.input_shape

    output_shape_Dataset = torch.flatten(Dataset[0][1]).shape[0]
    ouput_shape_overview = overview.data.output_shape1*overview.data.output_shape2*3

    if input_shape_Dataset != input_shape_overview or output_shape_Dataset != ouput_shape_overview:
        print(Fore.RED)
        print("Warning!: NN does not run with the latest data format")
        print(Style.RESET_ALL)

    return Dataset
