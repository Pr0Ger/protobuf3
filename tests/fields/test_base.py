from protobuf3.fields.base import BaseField
from protobuf3.fields.string import StringField
from protobuf3.message import Message
from unittest import TestCase


class TestBaseField(TestCase):
    def setUp(self):
        class EmptyMessage(Message):
            a = BaseField(field_number=1)

        class TestMessage(Message):
            a = StringField(field_number=1, repeated=True)

        raw_message = [
            0x0A, 0x07, 0x74, 0x65, 0x73, 0x74, 0x69, 0x6E, 0x67,
            0x0A, 0x08, 0x74, 0x65, 0x73, 0x74, 0x69, 0x6E, 0x67, 0x31
        ]

        self.empty_msg = EmptyMessage()
        self.repeated_msg = TestMessage()
        self.repeated_msg.parse_from_bytes(raw_message)

    def test_constructor_validation(self):
        self.assertRaises(AssertionError, BaseField, 'a')

    def test_default_value_handling(self):
        self.assertEqual(self.empty_msg.a, None)

    def test_get_repeated_field(self):
        self.assertEqual(type(self.repeated_msg.a), StringField)

    def test_len(self):
        self.assertEqual(2, len(self.repeated_msg.a))

    def test_get_item(self):
        self.assertEqual(self.repeated_msg.a[0], 'testing')
