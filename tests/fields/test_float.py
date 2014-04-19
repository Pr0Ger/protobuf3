from protobuf3.fields.float import FloatField
from protobuf3.message import Message
from unittest import TestCase


class TestFloatField(TestCase):
    def setUp(self):
        class FloatTestMessage(Message):
            a = FloatField(field_number=1)

        self.msg_cls = FloatTestMessage

    def test_get(self):
        msg = self.msg_cls()

        msg.parse_from_bytes(b'\r\x00 \xf1G')
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

        def failure_overflow():
            msg.a = 2 ** 40

        self.assertRaises(ValueError, failure)
        self.assertRaises(ValueError, failure_overflow)


