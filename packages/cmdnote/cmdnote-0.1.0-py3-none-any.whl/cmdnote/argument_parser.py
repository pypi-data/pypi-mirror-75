from argparse import ArgumentParser
from . import const


class Parser:
    """
    Parser of CLI arguments
    """

    def __init__(self):
        # create the top-level parser
        parser = ArgumentParser(prog='cmdnote',
                                description='cmdnote is a command line tool which stores '
                                            'your future commands.')
        subparsers = parser.add_subparsers(title='sub-commands', help='cmdnote sub-commands',
                                           dest='subcommand')

        # create the parser for the "func" command
        parser_func = subparsers.add_parser('func',
                                            help='print the cmdnote function for CLI initialization')

        # create the parser for the "append" command
        parser_append = subparsers.add_parser('append', help='append commands to the end of note')
        group_append = parser_append.add_mutually_exclusive_group(required=True)
        group_append.add_argument('-f', '--file', type=str,
                                  help='a script file that contains commands')
        group_append.add_argument('-c', '--command', type=str,
                                  help='a single command')

        # create the parser for the "insert" command
        parser_insert = subparsers.add_parser('insert',
                                              help='insert commands to the beginning of note')
        group_insert = parser_insert.add_mutually_exclusive_group(required=True)
        group_insert.add_argument('-f', '--file', type=str,
                                  help='a script file that contains commands')
        group_insert.add_argument('-c', '--command', type=str,
                                  help='a single command')

        # create the parser for the "list" command
        parser_list = subparsers.add_parser('list', help='list future commands')
        parser_list.add_argument('-a', '--all', action='store_true',
                                 help='list past and future commands')

        # create the parser for the "next" command
        parser_next = subparsers.add_parser('next', help='get the next command to run')

        # create the parser for the "prev" command
        parser_prev = subparsers.add_parser('prev', help='get the previous command to run')

        # create the parser for the "seek" command
        parser_seek = subparsers.add_parser('seek', help='set the note\'s current position')
        parser_seek.add_argument('index', type=int, help='command index')

        # create the parser for the "clear" command
        parser_clear = subparsers.add_parser('clear', help='clear future commands')
        parser_clear.add_argument('-a', '--all', action='store_true',
                                  help='clear past and future commands')

        # create the parser for the "play" command
        parser_play = subparsers.add_parser('play', help='run all future commands')
        parser_play.add_argument('-i', '--interval', type=float, default=1,
                                 help='interval in seconds between two commands')
        parser_play.add_argument('-d', '--delay', type=float, default=0.5,
                                 help='delay in seconds between showing and running a command')
        parser_play.add_argument('-r', '--repeat', type=int, default=1,
                                 help='number of times to run future commands repeatedly')

        # create the parser for the "config" command
        parser_config = subparsers.add_parser('config', help='configure cmdnote')
        parser_config.add_argument('-c', '--capacity', type=int,
                                   help='capacity of notebook, default {}'.format(
                                       const.CONFIG_DEFAULT_CAPACITY))

        self.parser = parser

    def parse_args(self):
        """Parse arguments or print help if no sub-command provided."""
        args = self.parser.parse_args()
        if args.subcommand is None:
            self.parser.print_help()
        return args
