from .base import BaseField
from protobuf3.wire_types import FIELD_FIXED64
from struct import pack, unpack


class Fixed64Field(BaseField):
    DEFAULT_VALUE = 0
    WIRE_TYPE = FIELD_FIXED64

    def _convert_to_final_type(self, value):
        return unpack('<Q', value)[0]

    def _convert_to_wire_type(self, value):
        return pack('<Q', value)

    def _validate(self, value):
        return isinstance(value, int) and 0 <= value < 2 ** 64
