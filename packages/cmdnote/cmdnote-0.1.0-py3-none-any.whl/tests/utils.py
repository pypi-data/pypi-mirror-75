from contextlib import contextmanager
from io import StringIO
import os
import sys
from cmdnote import system

TEST_FILE = os.path.join(os.path.dirname(__file__), 'test.sh')


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


@contextmanager
def captured_sys_stdout():
    new_out = StringIO()
    old_out = system.sys_stdout
    try:
        system.sys_stdout = new_out
        yield new_out
    finally:
        system.sys_stdout = old_out
