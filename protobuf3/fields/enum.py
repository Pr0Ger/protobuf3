from .base import BaseField
from enum import Enum
from protobuf3.wire_types import FIELD_VARINT


class EnumField(BaseField):
    WIRE_TYPE = FIELD_VARINT

    def __init__(self, enum_cls=None, **kwargs):
        if not(isinstance(enum_cls, type) and issubclass(enum_cls, Enum)):
            raise ValueError

        self.__cls = enum_cls
        super().__init__(**kwargs)

    @property
    def default_value(self):
        old_value = super().default_value
        if old_value:
            return old_value

        return next(iter(self.__cls))  # Hack to get first element from enum

    def _convert_to_final_type(self, value):
        return self.__cls(value)

    def _convert_to_wire_type(self, value):
        return value.value

    def _validate(self, value):
        return isinstance(value, self.__cls)
