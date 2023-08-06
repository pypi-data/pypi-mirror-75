class Parser:
    """
    Parser of commands
    """

    @staticmethod
    def parse_file(filename):
        """Parse commands from a file."""
        with open(filename, 'r') as f:
            content = f.read()
        return Parser.parse_content(content)

    @staticmethod
    def parse_content(content):
        """Parse commands from a multi-line string."""
        lines = content.split('\n')
        commands = []
        for line in lines:
            command = Parser.parse_command(line)
            if command:
                commands.append(command)
        return commands

    @staticmethod
    def parse_command(command):
        """Parse command from a single-line string."""
        command = command.rstrip('\n')
        if Parser.is_empty(command):
            return None
        return command

    @staticmethod
    def is_empty(command):
        """Check if a string is an empty command."""
        return str.isspace(command)
