from protobuf3.fields.base import BaseField
from protobuf3.fields.string import StringField
from protobuf3.message import Message
from unittest import TestCase


class TestBaseField(TestCase):
    def test_constructor_validation(self):
        self.assertRaises(AssertionError, BaseField, 'a')

    def test_default_value_handling(self):
        class EmptyMessage(Message):
            a = BaseField(field_number=1)

        msg = EmptyMessage()
        self.assertEqual(msg.a, None)

    def test_get_repeated_field(self):
        class TestMessage(Message):
            a = StringField(field_number=1, repeated=True)

        msg = TestMessage()
        self.assertRaises(ValueError, lambda: msg.a)
