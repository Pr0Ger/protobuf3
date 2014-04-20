from unittest import TestCase
from protobuf3.fields.uint64 import UInt64Field
from protobuf3.message import Message


class TestUInt64Field(TestCase):
    def setUp(self):
        class UInt64TestMessage(Message):
            a = UInt64Field(field_number=1)

        self.msg_cls = UInt64TestMessage

    def test_get(self):
        msg = self.msg_cls()

        msg.parse_from_bytes(b'\x08\xc0\xc4\x07')
        self.assertEqual(msg.a, 123456)

    def test_default_get(self):
        msg = self.msg_cls()

        self.assertEqual(msg.a, 0)

    def test_set(self):
        msg = self.msg_cls()

        msg.a = 2 ** 40
        self.assertEqual(msg.a, 2 ** 40)
        msg.encode_to_bytes()

    def test_invalid_set(self):
        msg = self.msg_cls()

        def failure():
            msg.a = '123'

        def overflow():
            msg.a = 2 ** 70

        self.assertRaises(ValueError, failure)
        self.assertRaises(ValueError, overflow)
