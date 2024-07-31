import time
import unittest

from pysearchlib.utils.util_bash import exec_cmd
from pysearchlib.utils.util_directory import make_dirs


class MyFileTestCase(unittest.TestCase):
    def test_mkdir(self):
        make_dirs("/Users/sunwu/SW-Research/p1_ch05/export_db")
