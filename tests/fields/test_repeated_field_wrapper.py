from protobuf3.fields.string import StringField
from protobuf3.message import Message
from unittest import TestCase


class TestRepeatedFieldWrapper(TestCase):
    def setUp(self):
        class TestMessage(Message):
            a = StringField(field_number=1, repeated=True)

        raw_message = [
            0x0A, 0x07, 0x74, 0x65, 0x73, 0x74, 0x69, 0x6E, 0x67,
            0x0A, 0x08, 0x74, 0x65, 0x73, 0x74, 0x69, 0x6E, 0x67, 0x31
        ]

        self.msg = TestMessage()
        self.msg.parse_from_bytes(raw_message)

    def test_get_item(self):
        self.assertEqual(self.msg.a[0], 'testing')
        self.assertEqual(self.msg.a[0], 'testing1')

    def test_len(self):
        self.assertEqual(len(self.msg.a), 2)
