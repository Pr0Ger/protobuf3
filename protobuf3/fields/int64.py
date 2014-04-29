from .base import BaseField
from protobuf3.wire_types import FIELD_VARINT


class Int64Field(BaseField):
    DEFAULT_VALUE = 0
    WIRE_TYPE = FIELD_VARINT

    def _convert_to_final_type(self, value):
        if value >= 2 ** 63:
            return -(2 ** 64 - value)

        return value

    def _convert_to_wire_type(self, value):
        if value < 0:
            return 2 ** 64 + value

        return value

    def _validate(self, value):
        return isinstance(value, int) and -2 ** 63 <= value < 2 ** 63
