import os
from . import const, exception


class Notebook:
    """
    Manager of cmdnote notebook
    """

    def __init__(self, notebook_file=const.NOTEBOOK_FILE, capacity=const.CONFIG_DEFAULT_CAPACITY):
        if not os.path.isfile(notebook_file):
            raise exception.NotebookFileNotFoundError('Notebook file not found', notebook_file)
        self.notebook_file = notebook_file
        self.capacity = capacity

    def read_commands(self):
        """Read commands and command_idx from notebook."""
        with open(self.notebook_file, 'r') as f:
            lines = f.readlines()
        if len(lines) == 0:
            return [], 0
        try:
            command_idx = int(lines[0])
        except ValueError:
            raise exception.NotebookFileFormatError('First line isn\'t an integer',
                                                    self.notebook_file)
        commands = [line.rstrip('\n') for line in lines[1:]]
        self._check_command_index(commands, command_idx)
        return commands, command_idx

    def write_commands(self, commands, command_idx):
        """Write commands and command_idx into notebook."""
        self._check_capacity(commands, command_idx)
        self._check_command_index(commands, command_idx)
        if len(commands) > self.capacity:
            diff = len(commands) - self.capacity
            command_idx -= diff
            commands = commands[diff:]
        lines = [str(command_idx) + '\n'] + [command + '\n' for command in commands]
        with open(self.notebook_file, 'w') as f:
            f.writelines(lines)

    def append_commands(self, commands):
        """Append commands to then end of notebook."""
        new_commands = commands
        if len(new_commands) == 0:
            return
        commands, command_idx = self.read_commands()
        commands.extend(new_commands)
        self.write_commands(commands, command_idx)

    def insert_commands(self, commands):
        """Insert commands to then beginning of notebook."""
        new_commands = commands
        if len(new_commands) == 0:
            return
        commands, command_idx = self.read_commands()
        commands[command_idx:command_idx] = new_commands
        self.write_commands(commands, command_idx)

    def next_command(self):
        """Return the next command in notebook."""
        commands, command_idx = self.read_commands()
        if len(commands) == command_idx:
            return None
        return commands[command_idx]

    def prev_command(self):
        """Return the previous command in notebook."""
        commands, command_idx = self.read_commands()
        if command_idx == 0:
            return None
        return commands[command_idx - 1]

    def move_commands(self, offset):
        """Move the command_idx by offset."""
        if offset == 0:
            return
        commands, command_idx = self.read_commands()
        command_idx += offset
        self.write_commands(commands, command_idx)

    def clear_commands(self, all=False):
        """Clear commands in notebook."""
        if all:
            commands, command_idx = [], 0
        else:
            commands, command_idx = self.read_commands()
            commands = commands[:command_idx]
        self.write_commands(commands, command_idx)

    def _check_command_index(self, commands, command_idx):
        """Check the command_idx is within the valid range."""
        if not 0 <= command_idx <= len(commands):
            raise exception.CommandIndexError(
                'Command index {} out of range [{}, {}]'.format(command_idx, 0, len(commands)),
                self.notebook_file)

    def _check_capacity(self, commands, command_idx):
        """Check the number of commands does not exceed capacity."""
        if len(commands[command_idx:]) > self.capacity:
            raise exception.NotebookCapacityError(
                'Commands number {} exceeds notebook capacity {}'.format(
                    len(commands[command_idx:]), self.capacity), self.notebook_file)
