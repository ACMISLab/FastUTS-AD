from unittest import TestCase

from pysearchlib.utils.util_qq import send_msg_to_qq


class TestQQ(TestCase):
    def test_qq(self):
        send_msg_to_qq("sjdfklsdjl")
