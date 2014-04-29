from .base import BaseField
from protobuf3.wire_types import FIELD_VARINT


class UInt32Field(BaseField):
    DEFAULT_VALUE = 0
    WIRE_TYPE = FIELD_VARINT

    def _convert_to_final_type(self, value):
        return value

    def _convert_to_wire_type(self, value):
        return value

    def _validate(self, value):
        return isinstance(value, int) and 0 <= value < 2 ** 32
