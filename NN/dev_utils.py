import builtins

from colorama import Back, Fore, Style, init

init(autoreset=True)


def diagnostics(message, type="diagnostics"):
    if type == "diagnostics":
        print(Fore.GREEN + "\ndiagnostics:", str(message), "\n")


builtins.diagnostics = diagnostics
