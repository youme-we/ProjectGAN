import builtins
import traceback

from colorama import Back, Fore, Style, init

init(autoreset=True)


def diagnostics(message, type="diagnostics"):
    if type == "error":
        print(Fore.RED + "\nerror:", traceback.format_exc())
    if type == "diagnostics":
        print(Fore.GREEN + "\ndiagnostics:", str(message), "\n")
    if type == "wrapper_info":
        print(Fore.YELLOW + "\nwrapper_info:", str(message), "\n")


builtins.diagnostics = diagnostics
