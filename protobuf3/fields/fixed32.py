from .base import BaseField
from protobuf3.wire_types import FIELD_FIXED32
from struct import pack, unpack


class Fixed32Field(BaseField):
    DEFAULT_VALUE = 0
    WIRE_TYPE = FIELD_FIXED32

    def _convert_to_final_type(self, value):
        return unpack('<L', value)[0]

    def _convert_to_wire_type(self, value):
        return pack('<L', value)

    def _validate(self, value):
        return isinstance(value, int) and 0 <= value < 2 ** 32
