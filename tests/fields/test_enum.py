from enum import Enum
from protobuf3.fields.enum import EnumField
from protobuf3.message import Message
from unittest import TestCase


class TestEnumField(TestCase):
    def setUp(self):
        class EnumTestMessage(Message):
            class Color(Enum):
                red = 1
                green = 2
                blue = 3

            a = EnumField(field_number=1, enum_cls=Color)

        self.msg_cls = EnumTestMessage

    def test_wrong_initialization(self):
        self.assertRaises(ValueError, EnumField, enum_cls=None)

    def test_get(self):
        msg = self.msg_cls()

        msg.parse_from_bytes(b'\x08\x02')
        self.assertEqual(msg.a, self.msg_cls.Color.green)

    def test_get_broken(self):
        msg = self.msg_cls()

        msg.parse_from_bytes(b'\x08\x08')
        self.assertRaises(ValueError, lambda: msg.a)

    def test_default_get(self):
        msg = self.msg_cls()

        self.assertEqual(msg.a, self.msg_cls.Color.red)

    def test_set(self):
        msg = self.msg_cls()

        msg.a = self.msg_cls.Color.blue
        self.assertEqual(msg.a, self.msg_cls.Color.blue)

    def test_invalid_set(self):
        msg = self.msg_cls()

        def failure():
            msg.a = 1

        self.assertRaises(ValueError, failure)
