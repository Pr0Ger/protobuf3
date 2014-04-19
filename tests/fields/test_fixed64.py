from protobuf3.fields.fixed64 import Fixed64Field
from protobuf3.message import Message
from unittest import TestCase


class TestFixed64Field(TestCase):
    def setUp(self):
        class Fixed64TestMessage(Message):
            a = Fixed64Field(field_number=1)

        self.msg_cls = Fixed64TestMessage

    def test_get(self):
        msg = self.msg_cls()

        msg.parse_from_bytes(b'\t\xd2\x02\x96I\x00\x00\x00\x00')
        self.assertEqual(msg.a, 1234567890)

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
            msg.a = 'test'

        def failure_negative():
            msg.a = -1

        def failure_overflow():
            msg.a = 2 ** 70

        self.assertRaises(ValueError, failure)
        self.assertRaises(ValueError, failure_negative)
        self.assertRaises(ValueError, failure_overflow)
