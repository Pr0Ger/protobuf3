from .base import BaseField
from protobuf3.wire_types import FIELD_VARINT


class BoolField(BaseField):
    DEFAULT_VALUE = False
    WIRE_TYPE = FIELD_VARINT

    def _convert_to_final_type(self, value):
        return bool(value)

    def _convert_to_wire_type(self, value):
        return int(bool(value))

    def _validate(self, value):
        return isinstance(value, (bool, int))
