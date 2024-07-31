import unittest

from pysearchlib.affiliation.generics import convert_vector_to_events
from pysearchlib.utils.util_time import RunningTime


@RunningTime
def run():
    for i in range(1000000):
        # 3.124541s
        convert_vector_to_events()


class TestUnit(unittest.TestCase):
    def test_a1(self):
        run()
