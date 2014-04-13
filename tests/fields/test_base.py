from protobuf3.fields.base import BaseField
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
