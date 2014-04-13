from protobuf3.message import Message, WireField
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

    def test_decode_varint(self):
        tmp = Message()

        data = [0b00000001]
        self.assertEqual(tmp._decode_varint(iter(data)), 1)

        data = [0b10010110,  0b00000001]
        self.assertEqual(tmp._decode_varint(iter(data)), 150)

        data = [0b10101100, 0b00000010]
        self.assertEqual(tmp._decode_varint(iter(data)), 300)

    def test_decode_raw_message(self):
        # FIELD_VARINT
        tmp = Message()
        data = [0x08, 0x96, 0x01]
        expected_message = {1: [WireField(type=Message.FIELD_VARINT, value=150)]}
        tmp._decode_raw_message(iter(data))
        self.assertDictEqual(tmp._Message__wire_message, expected_message)

        # FIELD_FIXED64
        tmp = Message()
        data = [0x09, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]
        expected_message = {
            1: [WireField(type=Message.FIELD_FIXED64, value=[0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08])]
        }
        tmp._decode_raw_message(iter(data))
        self.assertDictEqual(tmp._Message__wire_message, expected_message)

        # FIELD_VARIABLE_LENGTH
        tmp = Message()
        data = [0x12, 0x07, 0x74, 0x65, 0x73, 0x74, 0x69, 0x6E, 0x67]
        expected_message = {
            2: [WireField(type=Message.FIELD_VARIABLE_LENGTH, value=[0x74, 0x65, 0x73, 0x74, 0x69, 0x6E, 0x67])]
        }
        tmp._decode_raw_message(iter(data))
        self.assertDictEqual(tmp._Message__wire_message, expected_message)

        # FIELD_FIXED32
        tmp = Message()
        data = [0x0D, 0x01, 0x02, 0x03, 0x04]
        expected_message = {1: [WireField(type=Message.FIELD_FIXED32, value=[0x01, 0x02, 0x03, 0x04])]}
        tmp._decode_raw_message(iter(data))
        self.assertDictEqual(tmp._Message__wire_message, expected_message)

    def test_get_wire_values(self):
        tmp = Message()

        data = [0x08, 0x96, 0x01]
        tmp.parse_from_bytes(data)
        self.assertEqual(tmp._get_wire_values(1), [WireField(type=Message.FIELD_VARINT, value=150)])

    def test_set_wire_values(self):
        tmp = Message()

        tmp._set_wire_values(1, Message.FIELD_VARINT, 150)
        self.assertDictEqual(tmp._Message__wire_message, {1: [WireField(type=Message.FIELD_VARINT, value=150)]})

    def test_parse_from_bytes(self):
        tmp = Message()

        data = [0x08, 0x96, 0x01]
        expected_message = {1: [WireField(type=Message.FIELD_VARINT, value=150)]}
        tmp.parse_from_bytes(data)
        self.assertDictEqual(tmp._Message__wire_message, expected_message)
