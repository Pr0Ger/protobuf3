from protobuf3.fields.double import DoubleField
from protobuf3.message import Message
from unittest import TestCase


class TestDoubleField(TestCase):
    def setUp(self):
        class DoubleTestMessage(Message):
            a = DoubleField(field_number=1)

        self.msg_cls = DoubleTestMessage

    def test_get(self):
        msg = self.msg_cls()

        msg.parse_from_bytes(b'\t\x00\x00\x00\x00\x00$\xfe@')
        self.assertEqual(msg.a, 123456.0)

    def test_default_get(self):
        msg = self.msg_cls()

        self.assertEqual(msg.a, 0.0)

    def test_set(self):
        msg = self.msg_cls()

        msg.a = 1337
        self.assertEqual(msg.a, 1337)

    def test_invalid_set(self):
        msg = self.msg_cls()

        def failure():
            msg.a = 'test'

        self.assertRaises(ValueError, failure)
