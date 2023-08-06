from . import store
from .argument_parser import Parser
from .cmdnote import CmdNote


def main():
    store.ensure_default_files()
    args = Parser().parse_args()
    CmdNote().handle(args)


if __name__ == '__main__':
    main()
