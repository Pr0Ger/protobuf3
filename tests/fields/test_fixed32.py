from protobuf3.fields.fixed32 import Fixed32Field
from protobuf3.message import Message
from unittest import TestCase


class TestFixed32Field(TestCase):
    def setUp(self):
        class Fixed32TestMessage(Message):
            a = Fixed32Field(field_number=1)

        self.msg_cls = Fixed32TestMessage

    def test_get(self):
        msg = self.msg_cls()

        msg.parse_from_bytes(b'\r\xd2\x02\x96I')
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
            msg.a = 2 ** 40

        self.assertRaises(ValueError, failure)
        self.assertRaises(ValueError, failure_negative)
        self.assertRaises(ValueError, failure_overflow)

