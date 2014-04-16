from .base import BaseField
from protobuf3.message import Message


class StringField(BaseField):
    DEFAULT_VALUE = ""
    WIRE_TYPE = Message.FIELD_VARIABLE_LENGTH

    def _convert_to_final_type(self, value):
        return value.decode()

    def _convert_to_wire_type(self, value):
        return value.encode()

    def _validate(self, value):
        return isinstance(value, str)
