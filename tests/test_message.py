from protobuf3.message import Message
from unittest import TestCase


class TestMessage(TestCase):

    def test_decode_varint(self):
        tmp = Message()

        data = [0b00000001]
        self.assertEqual(tmp._decode_varint(iter(data)), 1)

        data = [0b10010110,  0b00000001]
        self.assertEqual(tmp._decode_varint(iter(data)), 150)

        data = [0b10101100, 0b00000010]
        self.assertEqual(tmp._decode_varint(iter(data)), 300)
