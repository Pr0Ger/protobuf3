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

        class RepeatedTestMessage(Message):
            c = MessageField(field_number=3, message_cls=InnerMessage, repeated=True)

        self.msg_cls = MessageTestMessage
        self.inner_msg_cls = InnerMessage
        self.repeated_msg_cls = RepeatedTestMessage

    def test_get(self):
        msg = self.msg_cls()

        msg.parse_from_bytes(b'\x1a\x03\x08\x96\x01')

        self.assertTrue(type(msg.c) == self.inner_msg_cls)
        self.assertEqual(msg.c.a, 150)

    def test_repeated_get(self):
        msg = self.repeated_msg_cls()

        msg.parse_from_bytes(b'\x1a\x03\x08\x96\x01\x1a\x04\x08\xc0\xc4\x07')

        self.assertEqual(msg.c[0].a, 150)
        self.assertEqual(msg.c[1].a, 123456)

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

    def test_set_repeated_field(self):
        msg = self.repeated_msg_cls()

        msg.parse_from_bytes(b'\x1a\x03\x08\x96\x01\x1a\x04\x08\xc0\xc4\x07')

        self.assertEqual(msg.c[0].a, 150)
        self.assertEqual(msg.c[1].a, 123456)

        msg.c[0].a = 123
        msg.c[1].a = 456

        self.assertEqual(msg.c[0].a, 123)
        self.assertEqual(msg.c[1].a, 456)
