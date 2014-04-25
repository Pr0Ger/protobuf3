from protobuf3.fields.int32 import Int32Field
from protobuf3.fields.message import MessageField
from protobuf3.message import Message
from unittest import TestCase


class TestMessageField(TestCase):
    def setUp(self):
        class InnerMessage(Message):
            a = Int32Field(field_number=1)

        class MessageTestMessage(Message):
            c = MessageField(field_number=3, message_cls=InnerMessage)

        self.msg_cls = MessageTestMessage
        self.inner_msg_cls = InnerMessage

    def test_get(self):
        msg = self.msg_cls()

        msg.parse_from_bytes(b'\x1a\x03\x08\x96\x01')

        self.assertTrue(type(msg.c) == self.inner_msg_cls)
        self.assertEqual(msg.c.a, 150)

    def test_default_get(self):
        msg = self.msg_cls()

        self.assertTrue(type(msg.c) == self.inner_msg_cls)
        self.assertEqual(msg.c.a, 0)

    def test_set(self):
        msg = self.msg_cls()

        msg.c.a = 150
        self.assertEqual(msg.c.a, 150)

    def test_invalid_set(self):
        msg = self.msg_cls()

        def failure():
            msg.c = '123'

        self.assertRaises(ValueError, failure)

