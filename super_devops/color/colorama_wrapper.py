from functools import partial

from colorama import Fore, init


class BaseColor(object):
    init()

    BLACK = partial(
        lambda info, color=Fore.RESET:
        color + str(info) + Fore.RESET,
        color=Fore.BLACK
    )

    BLUE = partial(
        lambda info, color=Fore.RESET:
        color + str(info) + Fore.RESET,
        color=Fore.BLUE
    )

    CYAN = partial(
        lambda info, color=Fore.RESET:
        color + str(info) + Fore.CYAN,
        color=Fore.CYAN
    )

    GREEN = partial(
        lambda info, color=Fore.GREEN:
        color + str(info) + Fore.GREEN,
        color=Fore.GREEN
    )

    MAGENTA = partial(
        lambda info, color=Fore.MAGENTA:
        color + str(info) + Fore.MAGENTA,
        color=Fore.MAGENTA
    )

    RED = partial(
        lambda info, color=Fore.RESET:
        color + str(info) + Fore.RESET,
        color=Fore.RED
    )

    RESET = partial(
        lambda info, color=Fore.RESET:
        color + str(info) + Fore.RESET,
        color=Fore.RESET
    )

    WHITE = partial(
        lambda info, color=Fore.WHITE:
        color + str(info) + Fore.RESET,
        color=Fore.WHITE
    )

    YELLOW = partial(
        lambda info, color=Fore.RESET:
        color + str(info) + Fore.RESET,
        color=Fore.YELLOW
    )