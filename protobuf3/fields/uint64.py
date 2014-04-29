from .base import BaseField
from protobuf3.wire_types import FIELD_VARINT


class UInt64Field(BaseField):
    DEFAULT_VALUE = 0
    WIRE_TYPE = FIELD_VARINT

    def _validate(self, value):
        return isinstance(value, int) and 0 <= value < 2 ** 64
