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
            b = StringField(field_number=2, repeated=True)

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
        self.assertEqual(len(self.repeated_msg.a), 2)

    def test_get_item(self):
        self.assertEqual(self.repeated_msg.a[0], 'testing')
        self.assertEqual(self.repeated_msg.a[1], 'testing1')

        self.assertRaises(IndexError, lambda: self.repeated_msg.a[3])

    def test_set_item(self):
        self.assertEqual(self.repeated_msg.a[0], 'testing')

        self.repeated_msg.a[0] = 'not testing'
        self.assertEqual(self.repeated_msg.a[0], 'not testing')

    def test_append(self):
        self.assertEqual(len(self.repeated_msg.b), 0)

        self.repeated_msg.b.append('test')
        self.assertEqual(len(self.repeated_msg.b), 1)
        self.assertEqual(self.repeated_msg.b[0], 'test')

    def test_insert(self):
        self.assertEqual(len(self.repeated_msg.a), 2)
        self.assertEqual(self.repeated_msg.a[0], 'testing')
        self.assertEqual(self.repeated_msg.a[1], 'testing1')

        self.repeated_msg.a.insert(1, 'middle testing')

        self.assertEqual(len(self.repeated_msg.a), 3)
        self.assertEqual(self.repeated_msg.a[0], 'testing')
        self.assertEqual(self.repeated_msg.a[1], 'middle testing')
        self.assertEqual(self.repeated_msg.a[2], 'testing1')

