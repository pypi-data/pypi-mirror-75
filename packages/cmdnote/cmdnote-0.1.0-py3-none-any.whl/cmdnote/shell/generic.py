import shlex
import colorama


class Generic:
    @staticmethod
    def quote(s):
        """Return a shell-escaped version of the string `s`."""
        return shlex.quote(s)

    @classmethod
    def echo_command(cls, command):
        """Return a generic shell command that echos the given `command`."""
        return 'echo $ {bold}{command}{reset}'.format(
            bold=colorama.Style.BRIGHT,
            command=cls.quote(command),
            reset=colorama.Style.RESET_ALL)

    @staticmethod
    def sleep(secs):
        """Return a generic shell command that sleeps `secs` seconds."""
        return 'sleep {}'.format(secs)

    @staticmethod
    def get_func():
        """Return a generic shell command that makes cmdnote eval its stdout."""
        return 'function cmdnote() { eval "$(command cmdnote "$@")"; }'
