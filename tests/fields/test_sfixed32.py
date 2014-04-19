from protobuf3.fields.sfixed32 import SFixed32Field
from protobuf3.message import Message
from unittest import TestCase


class TestSFixed32Field(TestCase):
    def setUp(self):
        class SFixed32TestMessage(Message):
            a = SFixed32Field(field_number=1)

        self.msg_cls = SFixed32TestMessage

    def test_get(self):
        msg = self.msg_cls()

        msg.parse_from_bytes(b'\r\xd2\x02\x96I')
        self.assertEqual(msg.a, 1234567890)

    def test_get_negative(self):
        msg = self.msg_cls()

        msg.parse_from_bytes(b'\r.\xfdi\xb6')
        self.assertEqual(msg.a, -1234567890)

    def test_default_get(self):
        msg = self.msg_cls()

        self.assertEqual(msg.a, 0)

    def test_set(self):
        msg = self.msg_cls()

        msg.a = 1337
        self.assertEqual(msg.a, 1337)

    def test_negative_set(self):
        msg = self.msg_cls()

        msg.a = -1337
        self.assertEqual(msg.a, -1337)

    def test_invalid_set(self):
        msg = self.msg_cls()

        def failure():
            msg.a = 'test'

        def failure_overflow():
            msg.a = 2 ** 40

        self.assertRaises(ValueError, failure)
        self.assertRaises(ValueError, failure_overflow)
