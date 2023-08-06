from . import const, ui, system
from .config import Config
from .notebook import Notebook
from .shell import shells, Generic
from .command_parser import Parser


class CmdNote:
    """
    Handler of cmdnote commands
    """

    def __init__(self, notebook_file=const.NOTEBOOK_FILE, config_file=const.CONFIG_FILE,
                 shell_type=None):
        self.args = (notebook_file, config_file, shell_type)
        self.configs = Config(config_file)
        capacity = int(self.configs.get_config(const.CONFIG_KEY_CAPACITY,
                                               const.CONFIG_DEFAULT_CAPACITY))
        self.notebook = Notebook(notebook_file, capacity=capacity)
        self.shell = shells.get(shell_type, Generic)
        self.parser = Parser()

    def handle(self, args):
        """Map sub-commands to handlers."""
        if args.subcommand == 'func':
            self.func()
        elif args.subcommand == 'append':
            self.append(file=args.file, command=args.command)
        elif args.subcommand == 'insert':
            self.insert(file=args.file, command=args.command)
        elif args.subcommand == 'list':
            self.list(args.all)
        elif args.subcommand == 'next':
            self.next()
        elif args.subcommand == 'prev':
            self.prev()
        elif args.subcommand == 'seek':
            self.seek(args.index)
        elif args.subcommand == 'clear':
            self.clear(args.all)
        elif args.subcommand == 'play':
            self.play(interval=args.interval, delay=args.delay, repeat=args.repeat)
        elif args.subcommand == 'config':
            self.config(**vars(args))

    def func(self):
        """Handler of `func` sub-command."""
        print(self.shell.get_func(), file=system.sys_stdout)

    def append(self, file=None, command=None):
        """Handler of `append` sub-command."""
        if file:
            commands = self.parser.parse_file(file)
            self.notebook.append_commands(commands)
        if command:
            commands = self.parser.parse_content(command)
            self.notebook.append_commands(commands)

    def insert(self, file=None, command=None):
        """Handler of `insert` sub-command."""
        if file:
            commands = self.parser.parse_file(file)
            self.notebook.insert_commands(commands)
        if command:
            commands = self.parser.parse_content(command)
            self.notebook.insert_commands(commands)

    def list(self, all=False):
        """Handler of `list` sub-command."""
        commands, command_idx = self.notebook.read_commands()
        if not all:
            commands = commands[command_idx:]
            command_idx = 0
        for i, command in enumerate(commands):
            ui.show_command_with_index(command, i - command_idx)

    def next(self):
        """Handler of `next` sub-command."""
        command = self.notebook.next_command()
        if command is None:
            print('We are done.')
            return
        ui.show_command_with_option(command)
        action = ui.get_action()
        if action == const.ACTION_EXECUTE:
            self.notebook.move_commands(1)
            print(command, file=system.sys_stdout)

    def prev(self):
        """Handler of `prev` sub-command."""
        command = self.notebook.prev_command()
        if command is None:
            print('No previous command.')
            return
        ui.show_command_with_option(command)
        action = ui.get_action()
        if action == const.ACTION_EXECUTE:
            print(command, file=system.sys_stdout)

    def seek(self, index):
        """Handler of `seek` sub-command."""
        self.notebook.move_commands(index)

    def clear(self, all=False):
        """Handler of `clear` sub-command."""
        self.notebook.clear_commands(all)

    def play(self, interval=1, delay=0.5, repeat=1):
        """Handler of `play` sub-command."""
        commands, command_idx = self.notebook.read_commands()
        commands = commands[command_idx:]
        self.notebook.move_commands(len(commands))
        commands *= repeat
        output = []
        for command in commands:
            output.append(self.shell.echo_command(command))
            output.append(self.shell.sleep(delay))
            output.append(command)
            output.append(self.shell.sleep(interval))
        output = output[:-1]
        print('\n'.join(output), file=system.sys_stdout)

    def config(self, **kwargs):
        """Handler of `config` sub-command."""
        keys = [const.CONFIG_KEY_CAPACITY]
        configs = self.configs.get_configs()
        if len([key for key in kwargs if key in keys and kwargs.get(key, None)]) == 0:
            for key in const.CONFIG_DEFAULT:
                if key not in configs:
                    configs[key] = const.CONFIG_DEFAULT[key]
            print(configs)
            return
        for key in keys:
            if kwargs.get(key, None):
                self.configs.set_config(const.CONFIG_KEY_CAPACITY, kwargs[key])
        try:
            self.reset()
        except Exception as e:
            self.configs.set_configs(configs)
            raise e

    def reset(self):
        """Re-initialize this class and reload notebook."""
        self.__init__(*self.args)
        commands, command_idx = self.notebook.read_commands()
        self.notebook.write_commands(commands, command_idx)
