from .base import BaseField
from protobuf3.wire_types import FIELD_FIXED64
from struct import pack, unpack


class DoubleField(BaseField):
    DEFAULT_VALUE = 0.0
    WIRE_TYPE = FIELD_FIXED64

    def _convert_to_final_type(self, value):
        return unpack('<d', value)[0]

    def _convert_to_wire_type(self, value):
        return pack('<d', value)

    def _validate(self, value):
        return isinstance(value, (float, int))
