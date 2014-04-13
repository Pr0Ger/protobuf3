from .base import BaseField


class StringField(BaseField):
    DEFAULT_VALUE = ""

    def _convert_to_final_type(self, value):
        return bytes(value).decode()

