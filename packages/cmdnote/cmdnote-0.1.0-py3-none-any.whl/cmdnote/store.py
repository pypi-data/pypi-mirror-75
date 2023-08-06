import os
from . import const


def ensure_default_files():
    """Create default notebook and config files if not exist."""
    os.makedirs(const.CMDNOTE_DIRECTORY, exist_ok=True)
    if not os.path.exists(const.NOTEBOOK_FILE):
        with open(const.NOTEBOOK_FILE, 'w'):
            pass
    if not os.path.exists(const.CONFIG_FILE):
        with open(const.CONFIG_FILE, 'w'):
            pass
