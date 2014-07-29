from .base import BaseField
from protobuf3.wire_types import FIELD_VARINT


class SInt32Field(BaseField):
    DEFAULT_VALUE = 0
    WIRE_TYPE = FIELD_VARINT

    def _convert_to_final_type(self, value):
        if value % 2:
            return -value // 2
        else:
            return value // 2

    def _convert_to_wire_type(self, value):
        return (value << 1) ^ (value >> 31)

    def _validate(self, value):
        return isinstance(value, int) and -2 ** 31 <= value < 2 ** 31
