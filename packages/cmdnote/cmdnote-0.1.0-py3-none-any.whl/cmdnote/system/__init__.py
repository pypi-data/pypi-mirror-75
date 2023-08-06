from .unix import *

sys_stdout = sys.stdout  # Backup the stdout.
sys.stdout = sys.stderr  # Redirect stdout to stderr.
