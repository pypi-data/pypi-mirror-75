import colorama
from . import const, system


def show_command_with_option(command):
    """Display a command with execute/abort options."""
    print('$ {bold}{command}{reset} [{green}enter{reset}/{red}ctrl+c{reset}]'.format(
        bold=colorama.Style.BRIGHT,
        command=command,
        reset=colorama.Style.RESET_ALL,
        green=colorama.Fore.GREEN,
        red=colorama.Fore.RED))


def show_command_with_index(command, command_idx):
    """Display a command with command_idx."""
    print('{blue}[{index}]{reset} {bold}{command}{reset}'.format(
        blue=colorama.Fore.BLUE,
        index=command_idx,
        reset=colorama.Style.RESET_ALL,
        bold=colorama.Style.BRIGHT,
        command=command))


def get_action():
    """Get user action by parsing input key."""
    while True:
        key = system.getch()
        if key in ['\n', '\r']:
            return const.ACTION_EXECUTE
        elif key in [const.KEY_CTRL_C, 'q']:
            return const.ACTION_ABORT
