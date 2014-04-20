from .base import BaseField
from protobuf3.message import Message


class UInt64Field(BaseField):
    DEFAULT_VALUE = 0
    WIRE_TYPE = Message.FIELD_VARINT

    def _validate(self, value):
        return isinstance(value, int) and 0 <= value < 2 ** 64
