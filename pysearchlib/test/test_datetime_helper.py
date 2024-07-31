from unittest import TestCase

from pysearchlib.application.datatime_helper import DateTimeHelper


class TestDTHelper(TestCase):
    def test_datetime_helper(self):
        dt=DateTimeHelper()
        dt.start()
        dt.end()
        print(dt.collect_metrics())