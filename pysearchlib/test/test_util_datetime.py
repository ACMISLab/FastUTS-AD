from unittest import TestCase

from pysearchlib.util_datetime import convert_timestamp_to_minutes


class TestDatetime(TestCase):
    def test_convert_timestamp_to_minutes(self):
        convert_timestamp_to_minutes(1475553900000000000)
