import json
from types import SimpleNamespace

import torch
from colorama import Back, Fore, Style


def device():
    device = (
        "cuda"
        if torch.cuda.is_available()
        else "mps" if torch.backends.mps.is_available() else "cpu"
    )

    return "cpu"


def load_json(file):
    with open(file, "r") as data_file:
        data = json.load(data_file, object_hook=lambda d: SimpleNamespace(**d))
    return data


def checking_data_actuality(Dataset, overview):
    input_shape_Dataset = Dataset[0][0].shape[0]
    input_shape_overview = overview.data.input_shape

    output_shape_Dataset = torch.flatten(Dataset[0][1]).shape[0]
    ouput_shape_overview = overview.data.output_shape1 * overview.data.output_shape2 * 3

    if (
        input_shape_Dataset != input_shape_overview
        or output_shape_Dataset != ouput_shape_overview
    ):
        print(Fore.RED)
        print("Warning!: NN does not run with the latest data format")
        print(Style.RESET_ALL)

    return Dataset


global isWindows

isWindows = False
try:
    from win32api import STD_INPUT_HANDLE
    from win32console import (
        ENABLE_ECHO_INPUT,
        ENABLE_LINE_INPUT,
        ENABLE_PROCESSED_INPUT,
        KEY_EVENT,
        GetStdHandle,
    )

    isWindows = True
except ImportError as e:
    import select
    import sys
    import termios


class KeyPoller:
    def __enter__(self):
        global isWindows
        if isWindows:
            self.readHandle = GetStdHandle(STD_INPUT_HANDLE)
            self.readHandle.SetConsoleMode(
                ENABLE_LINE_INPUT | ENABLE_ECHO_INPUT | ENABLE_PROCESSED_INPUT
            )

            self.curEventLength = 0
            self.curKeysLength = 0

            self.capturedChars = []
        else:
            # Save the terminal settings
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)

            # New terminal setting unbuffered
            self.new_term[3] = self.new_term[3] & ~termios.ICANON & ~termios.ECHO
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

        return self

    def __exit__(self, type, value, traceback):
        if isWindows:
            pass
        else:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    def poll(self):
        if isWindows:
            if not len(self.capturedChars) == 0:
                return self.capturedChars.pop(0)

            eventsPeek = self.readHandle.PeekConsoleInput(10000)

            if len(eventsPeek) == 0:
                return None

            if not len(eventsPeek) == self.curEventLength:
                for curEvent in eventsPeek[self.curEventLength :]:
                    if curEvent.EventType == KEY_EVENT:
                        if ord(curEvent.Char) == 0 or not curEvent.KeyDown:
                            pass
                        else:
                            curChar = str(curEvent.Char)
                            self.capturedChars.append(curChar)
                self.curEventLength = len(eventsPeek)

            if not len(self.capturedChars) == 0:
                return self.capturedChars.pop(0)
            else:
                return None
        else:
            dr, dw, de = select.select([sys.stdin], [], [], 0)
            if not dr == []:
                return sys.stdin.read(1)
            return None
