from protobuf3.fields.bytes import BytesField
from protobuf3.message import Message
from unittest import TestCase


class TestBytesField(TestCase):
    def setUp(self):
        class BytesTestMessage(Message):
            b = BytesField(field_number=2)

        self.msg_cls = BytesTestMessage

    def test_get(self):
        msg = self.msg_cls()

        msg.parse_from_bytes([0x12, 0x07, 0x74, 0x65, 0x73, 0x74, 0x69, 0x6E, 0x67])
        self.assertEqual(msg.b, b'testing')

    def test_default_get(self):
        msg = self.msg_cls()

        self.assertEqual(msg.b, b'')

    def test_set(self):
        msg = self.msg_cls()

        msg.b = b'test'
        self.assertEqual(msg.b, b'test')

    def test_set_string(self):
        msg = self.msg_cls()

        msg.b = 'test'
        self.assertEqual(msg.b, b'test')

    def test_invalid_set(self):
        msg = self.msg_cls()

        def failure():
            msg.b = 123

        self.assertRaises(ValueError, failure)
