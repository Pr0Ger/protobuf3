from protobuf3.fields.base import BaseField
from protobuf3.fields.message import MessageField
from protobuf3.fields.string import StringField
from protobuf3.list_wrapper import ListWrapper
from protobuf3.message import Message
from unittest import TestCase


class TestBaseField(TestCase):
    def setUp(self):
        class EmptyMessage(Message):
            a = BaseField(field_number=1)

        class TestMessage(Message):
            a = StringField(field_number=1, repeated=True)
            b = StringField(field_number=2, repeated=True)

        raw_message = bytes([
            0x0A, 0x07, 0x74, 0x65, 0x73, 0x74, 0x69, 0x6E, 0x67,
            0x0A, 0x08, 0x74, 0x65, 0x73, 0x74, 0x69, 0x6E, 0x67, 0x31
        ])

        self.empty_msg = EmptyMessage()
        self.repeated_msg = TestMessage()
        self.repeated_msg.parse_from_bytes(raw_message)

    def test_constructor_validation(self):
        self.assertRaises(AssertionError, BaseField, 'a')

    def test_default_value_handling(self):
        self.assertEqual(self.empty_msg.a, None)

    def test_custom_default_value(self):
        class TestMsg(Message):
            a = BaseField(field_number=1)
            b = BaseField(field_number=2, default=5)

        msg = TestMsg()

        self.assertEqual(msg.a, None)
        self.assertEqual(msg.b, 5)

    def test_invalid_custom_default_value(self):
        self.assertRaises(ValueError, StringField, field_number=1, default=0)

    def test_get_repeated_field(self):
        self.assertTrue(isinstance(self.repeated_msg.a, ListWrapper))

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

        self.repeated_msg.a[1] = 'not testing1'
        self.assertEqual(self.repeated_msg.a[1], 'not testing1')

    def test_append(self):
        self.assertEqual(len(self.repeated_msg.b), 0)

        self.repeated_msg.b.append('test')
        self.assertEqual(len(self.repeated_msg.b), 1)
        self.assertEqual(self.repeated_msg.b[0], 'test')

    def test_extend(self):
        self.assertEqual(len(self.repeated_msg.b), 0)

        self.repeated_msg.b.extend(['asd', 'qwe'])
        self.assertEqual(len(self.repeated_msg.b), 2)
        self.assertEqual(self.repeated_msg.b[0], 'asd')
        self.assertEqual(self.repeated_msg.b[1], 'qwe')

    def test_insert(self):
        self.assertEqual(len(self.repeated_msg.a), 2)
        self.assertEqual(self.repeated_msg.a[0], 'testing')
        self.assertEqual(self.repeated_msg.a[1], 'testing1')

        self.repeated_msg.a.insert(1, 'middle testing')

        self.assertEqual(len(self.repeated_msg.a), 3)
        self.assertEqual(self.repeated_msg.a[0], 'testing')
        self.assertEqual(self.repeated_msg.a[1], 'middle testing')
        self.assertEqual(self.repeated_msg.a[2], 'testing1')

    def test_concurrent_len_in_different_instances(self):
        class TestMsg(Message):
            a = StringField(field_number=1, repeated=True)

        msg_a = TestMsg()
        msg_a.a.append('a')
        msg_a.a.append('b')
        self.assertEqual(len(msg_a.a), 2)

        msg_b = TestMsg()
        msg_b.a.append('a')
        self.assertEqual(len(msg_b.a), 1)

        msg_a_field = msg_a.a
        msg_b_field = msg_b.a

        self.assertEqual(len(msg_a_field), 2)
        self.assertEqual(len(msg_b_field), 1)

    def test_add(self):
        class EmbMsg(Message):
            a = StringField(field_number=1)

        class TestMsg(Message):
            a = StringField(field_number=1, repeated=True)
            b = MessageField(field_number=2, repeated=True, message_cls=EmbMsg)

        msg = TestMsg()

        self.assertEqual(len(msg.a), 0)
        value = msg.a.add()
        self.assertTrue(isinstance(value, str))
        self.assertEqual(len(msg.a), 1)

        self.assertEqual(len(msg.b), 0)
        value = msg.b.add()
        self.assertTrue(isinstance(value, EmbMsg))
        self.assertEqual(len(msg.b), 1)

        value.a = 'asd'
        self.assertEqual(msg.b[0].a, 'asd')

    def test_repeated_equal(self):
        class TestMsg(Message):
            a = StringField(field_number=1, repeated=True)

        msg = TestMsg()
        msg.a.append('asd')
        msg.a.append('qwe')

        self.assertNotEqual(msg.a, 'asd')
        self.assertNotEqual(msg.a, ['asd'])
        self.assertNotEqual(msg.a, ['qwe', 'asd'])

        self.assertEqual(msg.a, ['asd', 'qwe'])
        self.assertEqual(msg.a, ('asd', 'qwe'))

    def test_repeated_del(self):
        class TestMsg(Message):
            a = StringField(field_number=1, repeated=True)

        msg = TestMsg()
        msg.a.append('asd')
        msg.a.append('qwe')
        msg.a.append('zxc')

        self.assertEqual(msg.a, ['asd', 'qwe', 'zxc'])

        del msg.a[1]

        self.assertEqual(msg.a, ['asd', 'zxc'])

    def test_repeated_clear(self):
        self.assertEqual(len(self.repeated_msg.a), 2)
        del self.repeated_msg.a[:]
        self.assertEqual(len(self.repeated_msg.a), 0)

    def test_repr(self):
        field = BaseField(field_number=1, required=True)

        self.assertEqual(repr(field), '<BaseField(id=1, required)>')
