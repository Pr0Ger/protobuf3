from unittest import TestCase
from protobuf3.fields.sint64 import SInt64Field
from protobuf3.message import Message


class TestSInt32Field(TestCase):
    def setUp(self):
        class SInt64TestMessage(Message):
            a = SInt64Field(field_number=1)

        self.msg_cls = SInt64TestMessage

    def test_get(self):
        msg = self.msg_cls()

        msg.parse_from_bytes(b'\x08\x80\x89\x0f')
        self.assertEqual(msg.a, 123456)

    def test_get_bounds(self):
        msg = self.msg_cls()

        msg.parse_from_bytes(b'\x08\xfe\xff\xff\xff\xff\xff\xff\xff\xff\x01')
        self.assertEqual(msg.a, 2 ** 63 - 1)

    def test_get_negative(self):
        msg = self.msg_cls()

        msg.parse_from_bytes(b'\x08\xff\x88\x0f')
        self.assertEqual(msg.a, -123456)

    def test_default_get(self):
        msg = self.msg_cls()

        self.assertEqual(msg.a, 0)

    def test_set(self):
        msg = self.msg_cls()

        msg.a = 1337
        self.assertEqual(msg.a, 1337)

    def test_set_negative(self):
        msg = self.msg_cls()

        msg.a = -1337
        self.assertEqual(msg.a, -1337)

    def test_invalid_set(self):
        msg = self.msg_cls()

        def failure():
            msg.a = '123'

        def overflow():
            msg.a = 2 ** 70

        self.assertRaises(ValueError, failure)
        self.assertRaises(ValueError, overflow)
