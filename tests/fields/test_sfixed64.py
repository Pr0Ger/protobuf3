from protobuf3.fields.sfixed64 import SFixed64Field
from protobuf3.message import Message
from unittest import TestCase


class TestSFixed64Field(TestCase):
    def setUp(self):
        class SFixed64TestMessage(Message):
            a = SFixed64Field(field_number=1)

        self.msg_cls = SFixed64TestMessage

    def test_get(self):
        msg = self.msg_cls()

        msg.parse_from_bytes(b'\t\xd2\x02\x96I\x00\x00\x00\x00')
        self.assertEqual(msg.a, 1234567890)

    def test_get_negative(self):
        msg = self.msg_cls()

        msg.parse_from_bytes(b'\t.\xfdi\xb6\xff\xff\xff\xff')
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
            msg.a = 2 ** 70

        self.assertRaises(ValueError, failure)
        self.assertRaises(ValueError, failure_overflow)

