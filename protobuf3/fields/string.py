from .base import BaseField
from protobuf3.wire_types import FIELD_VARIABLE_LENGTH


class StringField(BaseField):
    DEFAULT_VALUE = ""
    WIRE_TYPE = FIELD_VARIABLE_LENGTH

    def _convert_to_final_type(self, value):
        return value.decode()

    def _convert_to_wire_type(self, value):
        return value.encode()

    def _validate(self, value):
        return isinstance(value, str)
