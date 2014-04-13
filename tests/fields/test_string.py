from protobuf3.fields.string import StringField
from protobuf3.message import Message
from unittest import TestCase


class TestStringField(TestCase):
    def setUp(self):
        class StringTestMessage(Message):
            b = StringField(field_number=2)

        self.msg_cls = StringTestMessage

    def test_get(self):
        msg = self.msg_cls()

        msg.parse_from_bytes([0x12, 0x07, 0x74, 0x65, 0x73, 0x74, 0x69, 0x6E, 0x67])
        self.assertEqual(msg.b, 'testing')

    def test_default_get(self):
        msg = self.msg_cls()

        self.assertEqual(msg.b, '')

    def test_set(self):
        msg = self.msg_cls()

        msg.b = 'test'
        self.assertEqual(msg.b, 'test')

    def test_invalid_set(self):
        msg = self.msg_cls()

        def failure():
            msg.b = 123

        self.assertRaises(ValueError, failure)
