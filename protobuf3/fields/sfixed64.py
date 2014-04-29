from .base import BaseField
from protobuf3.wire_types import FIELD_FIXED64
from struct import pack, unpack


class SFixed64Field(BaseField):
    DEFAULT_VALUE = 0
    WIRE_TYPE = FIELD_FIXED64

    def _convert_to_final_type(self, value):
        return unpack('<q', value)[0]

    def _convert_to_wire_type(self, value):
        return pack('<q', value)

    def _validate(self, value):
        return isinstance(value, int) and -2 ** 63 <= value < 2 ** 63
