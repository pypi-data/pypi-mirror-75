from unittest import TestCase
from unittest.mock import patch
import tempfile
from cmdnote import CmdNote, const, exception
from .utils import *


class TempCmdNote():
    def __enter__(self):
        self.notebook_fd = tempfile.NamedTemporaryFile()
        self.config_fd = tempfile.NamedTemporaryFile()
        return CmdNote(self.notebook_fd.name, self.config_fd.name)

    def __exit__(self, type, value, traceback):
        self.notebook_fd.close()
        self.config_fd.close()


class TestCmdNote(TestCase):
    def test_func(self):
        with TempCmdNote() as cmdnote:
            with captured_sys_stdout() as sysout:
                cmdnote.func()
                output = sysout.getvalue().strip()
                self.assertEqual(output, 'function cmdnote() { eval "$(command cmdnote "$@")"; }')

    def test_append(self):
        with TempCmdNote() as cmdnote:
            cmdnote.append(None, None)
            commands, command_idx = cmdnote.notebook.read_commands()
            self.assertEqual(len(commands), 0)
            self.assertEqual(command_idx, 0)
        with TempCmdNote() as cmdnote:
            cmdnote.append(TEST_FILE, None)
            commands, command_idx = cmdnote.notebook.read_commands()
            self.assertEqual(len(commands), 4)
            self.assertEqual(command_idx, 0)
        with TempCmdNote() as cmdnote:
            cmdnote.append(None, 'echo "hello"\nls -l')
            commands, command_idx = cmdnote.notebook.read_commands()
            self.assertEqual(len(commands), 2)
            self.assertEqual(command_idx, 0)
        with TempCmdNote() as cmdnote:
            cmdnote.append(TEST_FILE, None)
            cmdnote.append(None, 'echo "hello"')
            commands, command_idx = cmdnote.notebook.read_commands()
            self.assertEqual(len(commands), 5)
            self.assertEqual(command_idx, 0)
            self.assertEqual(commands[0], 'ls -l')
            self.assertEqual(commands[-1], 'echo "hello"')

    def test_insert(self):
        with TempCmdNote() as cmdnote:
            cmdnote.insert(None, None)
            commands, command_idx = cmdnote.notebook.read_commands()
            self.assertEqual(len(commands), 0)
            self.assertEqual(command_idx, 0)
        with TempCmdNote() as cmdnote:
            cmdnote.insert(TEST_FILE, None)
            commands, command_idx = cmdnote.notebook.read_commands()
            self.assertEqual(len(commands), 4)
            self.assertEqual(command_idx, 0)
        with TempCmdNote() as cmdnote:
            cmdnote.insert(None, 'echo "hello"\nls -l')
            commands, command_idx = cmdnote.notebook.read_commands()
            self.assertEqual(len(commands), 2)
            self.assertEqual(command_idx, 0)
        with TempCmdNote() as cmdnote:
            cmdnote.insert(TEST_FILE, None)
            cmdnote.insert(None, 'echo "hello"')
            commands, command_idx = cmdnote.notebook.read_commands()
            self.assertEqual(len(commands), 5)
            self.assertEqual(command_idx, 0)
            self.assertEqual(commands[0], 'echo "hello"')
            self.assertEqual(commands[-1], 'echo $MY_ENV_VAR')

    def test_list(self):
        with TempCmdNote() as cmdnote:
            cmdnote.append(TEST_FILE, None)
            with captured_output() as (out, err):
                cmdnote.list()
                output = out.getvalue().strip()
                self.assertEqual(len(output.split('\n')), 4)
        with TempCmdNote() as cmdnote:
            cmdnote.append(TEST_FILE, None)
            cmdnote.notebook.move_commands(1)
            with captured_output() as (out, err):
                cmdnote.list()
                output = out.getvalue().strip()
                self.assertEqual(len(output.split('\n')), 3)
        with TempCmdNote() as cmdnote:
            cmdnote.append(TEST_FILE, None)
            cmdnote.notebook.move_commands(1)
            with captured_output() as (out, err):
                cmdnote.list(True)
                output = out.getvalue().strip()
                self.assertEqual(len(output.split('\n')), 4)

    def test_next(self):
        with TempCmdNote() as cmdnote:
            cmdnote.append(TEST_FILE, None)
            with captured_output() as (out, err):
                with captured_sys_stdout() as sysout:
                    with patch('cmdnote.ui.get_action', lambda *args: const.ACTION_EXECUTE):
                        cmdnote.next()
                        self.assertTrue('ls -l' in out.getvalue().strip())
                        self.assertTrue('ls -l' in sysout.getvalue().strip())
            commands, command_idx = cmdnote.notebook.read_commands()
            self.assertEqual(len(commands), 4)
            self.assertEqual(command_idx, 1)
        with TempCmdNote() as cmdnote:
            cmdnote.append(TEST_FILE, None)
            with captured_output() as (out, err):
                with captured_sys_stdout() as sysout:
                    with patch('cmdnote.ui.get_action', lambda *args: const.ACTION_ABORT):
                        cmdnote.next()
                        self.assertTrue('ls -l' in out.getvalue().strip())
                        self.assertTrue('ls -l' not in sysout.getvalue().strip())
            commands, command_idx = cmdnote.notebook.read_commands()
            self.assertEqual(len(commands), 4)
            self.assertEqual(command_idx, 0)
        with TempCmdNote() as cmdnote:
            with captured_output() as (out, err):
                with patch('cmdnote.ui.get_action', lambda *args: const.ACTION_EXECUTE):
                    cmdnote.next()
            commands, command_idx = cmdnote.notebook.read_commands()
            self.assertEqual(len(commands), 0)
            self.assertEqual(command_idx, 0)

    def test_prev(self):
        with TempCmdNote() as cmdnote:
            cmdnote.append(TEST_FILE, None)
            cmdnote.notebook.move_commands(1)
            with captured_output() as (out, err):
                with captured_sys_stdout() as sysout:
                    with patch('cmdnote.ui.get_action', lambda *args: const.ACTION_EXECUTE):
                        cmdnote.prev()
                        self.assertTrue('ls -l' in out.getvalue().strip())
                        self.assertTrue('ls -l' in sysout.getvalue().strip())
            commands, command_idx = cmdnote.notebook.read_commands()
            self.assertEqual(len(commands), 4)
            self.assertEqual(command_idx, 1)
        with TempCmdNote() as cmdnote:
            cmdnote.append(TEST_FILE, None)
            cmdnote.notebook.move_commands(1)
            with captured_output() as (out, err):
                with captured_sys_stdout() as sysout:
                    with patch('cmdnote.ui.get_action', lambda *args: const.ACTION_ABORT):
                        cmdnote.prev()
                        self.assertTrue('ls -l' in out.getvalue().strip())
                        self.assertTrue('ls -l' not in sysout.getvalue().strip())
            commands, command_idx = cmdnote.notebook.read_commands()
            self.assertEqual(len(commands), 4)
            self.assertEqual(command_idx, 1)
        with TempCmdNote() as cmdnote:
            with captured_output() as (out, err):
                with patch('cmdnote.ui.get_action', lambda *args: const.ACTION_EXECUTE):
                    cmdnote.prev()
            commands, command_idx = cmdnote.notebook.read_commands()
            self.assertEqual(len(commands), 0)
            self.assertEqual(command_idx, 0)

    def test_seek(self):
        with TempCmdNote() as cmdnote:
            cmdnote.append(TEST_FILE, None)
            cmdnote.seek(2)
            commands, command_idx = cmdnote.notebook.read_commands()
            self.assertEqual(len(commands), 4)
            self.assertEqual(command_idx, 2)
        with TempCmdNote() as cmdnote:
            cmdnote.append(TEST_FILE, None)
            cmdnote.notebook.move_commands(2)
            cmdnote.seek(-1)
            commands, command_idx = cmdnote.notebook.read_commands()
            self.assertEqual(len(commands), 4)
            self.assertEqual(command_idx, 1)

    def test_clear(self):
        with TempCmdNote() as cmdnote:
            cmdnote.append(TEST_FILE, None)
            cmdnote.clear()
            commands, command_idx = cmdnote.notebook.read_commands()
            self.assertEqual(len(commands), 0)
            self.assertEqual(command_idx, 0)
        with TempCmdNote() as cmdnote:
            cmdnote.append(TEST_FILE, None)
            cmdnote.notebook.move_commands(1)
            cmdnote.clear()
            commands, command_idx = cmdnote.notebook.read_commands()
            self.assertEqual(len(commands), 1)
            self.assertEqual(command_idx, 1)
        with TempCmdNote() as cmdnote:
            cmdnote.append(TEST_FILE, None)
            cmdnote.notebook.move_commands(1)
            cmdnote.clear(True)
            commands, command_idx = cmdnote.notebook.read_commands()
            self.assertEqual(len(commands), 0)
            self.assertEqual(command_idx, 0)

    def test_play(self):
        with TempCmdNote() as cmdnote:
            cmdnote.append(TEST_FILE, None)
            with captured_sys_stdout() as sysout:
                cmdnote.play()
                output = sysout.getvalue().strip()
                self.assertEqual(output.count('ls -l'), 2)
            commands, command_idx = cmdnote.notebook.read_commands()
            self.assertEqual(len(commands), 4)
            self.assertEqual(command_idx, 4)
        with TempCmdNote() as cmdnote:
            cmdnote.append(TEST_FILE, None)
            with captured_sys_stdout() as sysout:
                cmdnote.play(repeat=5)
                output = sysout.getvalue().strip()
                self.assertEqual(output.count('ls -l'), 10)
            commands, command_idx = cmdnote.notebook.read_commands()
            self.assertEqual(len(commands), 4)
            self.assertEqual(command_idx, 4)

    def test_config(self):
        with TempCmdNote() as cmdnote:
            cmdnote.append(TEST_FILE, None)
            cmdnote.notebook.move_commands(3)
            cmdnote.config(capacity=2)
            commands, command_idx = cmdnote.notebook.read_commands()
            self.assertEqual(len(commands), 2)
            self.assertEqual(command_idx, 1)
        with TempCmdNote() as cmdnote:
            cmdnote.append(TEST_FILE, None)
            cmdnote.notebook.move_commands(1)
            self.assertRaises(exception.NotebookCapacityError, cmdnote.config, capacity=2)
            commands, command_idx = cmdnote.notebook.read_commands()
            self.assertEqual(len(commands), 4)
            self.assertEqual(command_idx, 1)
        with TempCmdNote() as cmdnote:
            cmdnote.append(TEST_FILE, None)
            with captured_output() as (out, err):
                cmdnote.config()
                output = out.getvalue().strip()
                self.assertTrue('capacity' in eval(output))
