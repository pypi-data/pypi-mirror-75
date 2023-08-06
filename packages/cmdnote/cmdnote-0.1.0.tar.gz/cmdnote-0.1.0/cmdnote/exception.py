class NotebookFileNotFoundError(FileNotFoundError):
    """Raised when the notebook file is not found."""


class ConfigFileNotFoundError(FileNotFoundError):
    """Raised when the config file is not found."""


class NotebookFileFormatError(ValueError):
    """Raised when the notebook file has incorrect format."""


class ConfigFileFormatError(ValueError):
    """Raised when the config file has incorrect format."""


class CommandIndexError(IndexError):
    """Raised when the command index is out of range."""


class NotebookCapacityError(ValueError):
    """Raised when the number commands exceeds notebook capacity."""
