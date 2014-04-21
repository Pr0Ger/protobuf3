from unittest import TestCase
from protobuf3.fields.int64 import Int64Field
from protobuf3.message import Message


class TestInt64Field(TestCase):
    def setUp(self):
        class Int64TestMessage(Message):
            a = Int64Field(field_number=1)

        self.msg_cls = Int64TestMessage

    def test_get(self):
        msg = self.msg_cls()

        msg.parse_from_bytes(b'\x08\xc0\xc4\x07')
        self.assertEqual(msg.a, 123456)

    def test_get_bounds(self):
        msg = self.msg_cls()

        msg.parse_from_bytes(b'\x08\xff\xff\xff\xff\xff\xff\xff\xff\x7f')
        self.assertEqual(msg.a, 2 ** 63 - 1)

        msg.parse_from_bytes(b'\x08\x80\x80\x80\x80\x80\x80\x80\x80\x80\x01')
        self.assertEqual(msg.a, -(2 ** 63))

    def test_get_negative(self):
        msg = self.msg_cls()

        msg.parse_from_bytes(b'\x08\xc0\xbb\xf8\xff\xff\xff\xff\xff\xff\x01')
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

