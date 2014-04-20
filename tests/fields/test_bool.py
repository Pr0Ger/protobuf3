from protobuf3.fields.bool import BoolField
from protobuf3.message import Message
from unittest import TestCase


class TestBoolField(TestCase):
    def setUp(self):
        class BoolTestMessage(Message):
            a = BoolField(field_number=1)

        self.msg_cls = BoolTestMessage

    def test_get(self):
        msg = self.msg_cls()

        msg.parse_from_bytes(b'\x08\x01')
        self.assertEqual(msg.a, True)

    def test_default_get(self):
        msg = self.msg_cls()

        self.assertEqual(msg.a, False)

    def test_set(self):
        msg = self.msg_cls()

        msg.a = True
        self.assertEqual(msg.a, True)

    def test_invalid_set(self):
        msg = self.msg_cls()

        def failure():
            msg.a = '123'

        self.assertRaises(ValueError, failure)
