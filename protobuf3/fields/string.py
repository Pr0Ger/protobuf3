from .base import BaseField


class StringField(BaseField):
    DEFAULT_VALUE = ""
    WIRE_TYPE = 2

    def _convert_to_final_type(self, value):
        return bytes(value).decode()

    def _convert_to_wire_type(self, value):
        return value.encode()

    def _validate(self, value):
        return isinstance(value, str)
