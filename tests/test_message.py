from protobuf3.fields.string import StringField
from protobuf3.message import Message, WireField
from protobuf3.wire_types import FIELD_VARINT, FIELD_FIXED64, FIELD_VARIABLE_LENGTH, FIELD_FIXED32
from unittest import TestCase


class TestMessage(TestCase):

    def test_decode_field_signature(self):
        tmp = Message()

        data = [0b0001000]
        self.assertEqual(tmp._decode_field_signature(iter(data)), (0, 1, None))

        data = [0x12, 0x07]
        self.assertEqual(tmp._decode_field_signature(iter(data)), (2, 2, 7))

        data = [0b00001011]
        self.assertRaises(NotImplementedError, tmp._decode_field_signature, iter(data))

        data = [0b00001111]
        self.assertRaises(ValueError, tmp._decode_field_signature, iter(data))

    def test_encode_field_signature(self):
        tmp = Message()

        self.assertEqual(tmp._encode_field_signature(0, 1), b'\x08')
        self.assertEqual(tmp._encode_field_signature(2, 2, 7), b'\x12\x07')
        self.assertRaises(ValueError, tmp._encode_field_signature, 10, 1)
        self.assertRaises(AssertionError, tmp._encode_field_signature, 2, 2)

    def test_decode_varint(self):
        tmp = Message()

        data = [0b00000001]
        self.assertEqual(tmp._decode_varint(iter(data)), 1)

        data = [0b10010110,  0b00000001]
        self.assertEqual(tmp._decode_varint(iter(data)), 150)

        data = [0b10101100, 0b00000010]
        self.assertEqual(tmp._decode_varint(iter(data)), 300)

    def test_encode_varint(self):
        tmp = Message()

        self.assertEqual(tmp._encode_varint(1), b'\x01')
        self.assertEqual(tmp._encode_varint(150), b'\x96\x01')
        self.assertEqual(tmp._encode_varint(300), b'\xAC\x02')

    def test_decode_raw_message(self):
        # FIELD_VARINT
        tmp = Message()
        data = [0x08, 0x96, 0x01]
        expected_message = {1: [WireField(type=FIELD_VARINT, value=150)]}
        tmp._decode_raw_message(iter(data))
        self.assertDictEqual(tmp._Message__wire_message, expected_message)

        # FIELD_FIXED64
        tmp = Message()
        data = [0x09, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]
        expected_message = {
            1: [WireField(type=FIELD_FIXED64, value=b'\x01\x02\x03\x04\x05\x06\x07\x08')]
        }
        tmp._decode_raw_message(iter(data))
        self.assertDictEqual(tmp._Message__wire_message, expected_message)

        # FIELD_VARIABLE_LENGTH
        tmp = Message()
        data = [0x12, 0x07, 0x74, 0x65, 0x73, 0x74, 0x69, 0x6E, 0x67]
        expected_message = {
            2: [WireField(type=FIELD_VARIABLE_LENGTH, value=b'testing')]
        }
        tmp._decode_raw_message(iter(data))
        self.assertDictEqual(tmp._Message__wire_message, expected_message)

        # FIELD_FIXED32
        tmp = Message()
        data = [0x0D, 0x01, 0x02, 0x03, 0x04]
        expected_message = {1: [WireField(type=FIELD_FIXED32, value=b'\x01\x02\x03\x04')]}
        tmp._decode_raw_message(iter(data))
        self.assertDictEqual(tmp._Message__wire_message, expected_message)

    def test_decode_incorrect_field_signature(self):
        class StringTestMessage(Message):
            b = StringField(field_number=1)

        msg = StringTestMessage()
        data = [0x08, 0x96, 0x01]
        self.assertRaises(ValueError, msg._decode_raw_message, iter(data))

    def test_decode_repeated_field_with_different_types(self):
        raw_message = [
            0x08, 0x96, 0x01,
            0x0D, 0x01, 0x02, 0x03, 0x04
        ]

        msg = Message()
        self.assertRaises(ValueError, msg.parse_from_bytes, raw_message)

    def test_check_required_fields(self):
        class StringTestMessage(Message):
            b = StringField(field_number=1, required=1)

        msg = StringTestMessage()
        self.assertRaises(KeyError, msg._check_required_fields)

    def test_get_wire_values(self):
        tmp = Message()

        data = [0x08, 0x96, 0x01]
        tmp.parse_from_bytes(data)
        self.assertEqual(tmp._get_wire_values(1), [WireField(type=FIELD_VARINT, value=150)])

    def test_set_wire_values(self):
        tmp = Message()

        tmp._set_wire_values(1, FIELD_VARINT, 150)
        self.assertDictEqual(tmp._Message__wire_message, {1: [WireField(type=FIELD_VARINT, value=150)]})

    def test_parse_from_bytes(self):
        tmp = Message()

        data = [0x08, 0x96, 0x01]
        expected_message = {1: [WireField(type=FIELD_VARINT, value=150)]}
        tmp.parse_from_bytes(data)
        self.assertDictEqual(tmp._Message__wire_message, expected_message)

    def test_encode_to_bytes(self):
        class EncodedMessage(Message):
            a = StringField(field_number=2)

        msg = EncodedMessage()
        msg.a = 'test'

        expected = b'\x12\x04\x74\x65\x73\x74'

        self.assertEqual(msg.encode_to_bytes(), expected)

    def test_encode_to_bytes_varint(self):
        msg = Message()
        msg.parse_from_bytes(b'\x08\x96\x01')

        self.assertEqual(msg.encode_to_bytes(), b'\x08\x96\x01')

    def test_encode_to_bytes_repeated_order(self):
        class EncodedMessage(Message):
            a = StringField(field_number=2, repeated=True)

        msg = EncodedMessage()
        msg.a.append('test')
        msg.a.append('test1')

        expected = b'\x12\x04\x74\x65\x73\x74\x12\x05\x74\x65\x73\x74\x31'

        self.assertEqual(msg.encode_to_bytes(), expected)

    def test_encode_ignore_unknown(self):
        class EncodedMessage(Message):
            a = StringField(field_number=2)

        # Two fields: 1: int, 2: str
        original_msg = b'\x08\x96\x01\x12\x07\x74\x65\x73\x74\x69\x6E\x67'

        msg = EncodedMessage()

        msg.parse_from_bytes(original_msg)

        self.assertEqual(msg.encode_to_bytes(), original_msg)
        self.assertEqual(msg.encode_to_bytes(True), b'\x12\x07\x74\x65\x73\x74\x69\x6E\x67')

    def test_add_field(self):
        class TestMsg(Message):
            pass
        TestMsg.add_field('a', StringField(field_number=2, optional=True))

        msg = TestMsg()
        msg.parse_from_bytes(b'\x12\x07\x74\x65\x73\x74\x69\x6E\x67')

        self.assertTrue(hasattr(msg, 'a'))
        self.assertEqual(msg.a, 'testing')

    def test_contains(self):
        class TestMsg(Message):
            a = StringField(field_number=2, optional=True)

        msg = TestMsg()

        self.assertEqual('b' in msg, False)

        self.assertEqual('a' in msg, False)

        msg.parse_from_bytes(b'\x12\x07\x74\x65\x73\x74\x69\x6E\x67')
        self.assertEqual('a' in msg, True)
