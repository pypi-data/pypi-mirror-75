from unittest import TestCase
from unittest.mock import patch
from cmdnote.main import main
from .utils import *


class Test(TestCase):
    def test_main(self):
        with patch('sys.argv', ['cmdnote']):
            with captured_output() as (out, err):
                main()
                output = out.getvalue().strip()
                self.assertTrue(output.startswith('usage'))
