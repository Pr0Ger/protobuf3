from .base import BaseField
from protobuf3.wire_types import FIELD_FIXED32
from struct import pack, unpack


class FloatField(BaseField):
    DEFAULT_VALUE = 0.0
    WIRE_TYPE = FIELD_FIXED32

    def _convert_to_final_type(self, value):
        return unpack('<f', value)[0]

    def _convert_to_wire_type(self, value):
        return pack('<f', value)

    def _validate(self, value):
        return isinstance(value, (float, int))
