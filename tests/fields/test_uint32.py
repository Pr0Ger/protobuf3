from unittest import TestCase
from protobuf3.fields.uint32 import UInt32Field
from protobuf3.message import Message


class TestUInt32Field(TestCase):
    def setUp(self):
        class UInt32TestMessage(Message):
            a = UInt32Field(field_number=1)

        self.msg_cls = UInt32TestMessage

    def test_get(self):
        msg = self.msg_cls()

        msg.parse_from_bytes(b'\x08\xc0\xc4\x07')
        self.assertEqual(msg.a, 123456)

    def test_default_get(self):
        msg = self.msg_cls()

        self.assertEqual(msg.a, 0)

    def test_set(self):
        msg = self.msg_cls()

        msg.a = 1337
        self.assertEqual(msg.a, 1337)

    def test_invalid_set(self):
        msg = self.msg_cls()

        def failure():
            msg.a = '123'

        def overflow():
            msg.a = 2 ** 40

        self.assertRaises(ValueError, failure)
        self.assertRaises(ValueError, overflow)
