from protobuf3.list_wrapper import ListWrapper


class BaseField(object):
    DEFAULT_VALUE = None
    WIRE_TYPE = -1

    def __init__(self, field_number=None, required=False, optional=False, repeated=False, default=None):
        assert isinstance(field_number, int)

        self.__field_name = "undefined"
        self.__field_number = field_number
        self.__required = required
        self.__optional = optional
        self.__repeated = repeated

        if (default is not None) and (not self._validate(default)):
            raise ValueError
        self.__default = default

    @property
    def field_name(self):
        return self.__field_name

    @field_name.setter
    def field_name(self, value):
        self.__field_name = value

    @property
    def field_number(self):
        return self.__field_number

    @property
    def required(self):
        return self.__required

    @property
    def optional(self):
        return self.__optional

    @property
    def repeated(self):
        return self.__repeated

    @property
    def default_value(self):
        if self.__default:
            return self.__default
        return self.DEFAULT_VALUE

    def _convert_to_final_type(self, value):
        return value

    def _convert_to_wire_type(self, value):
        return value

    def _validate(self, value):
        return True

    def __get__(self, instance, owner):
        if self.__repeated:
            return ListWrapper(instance, self)
        else:
            wire_values = instance._get_wire_values(self.__field_number)

            if not wire_values:
                final_value = self.default_value
            else:
                final_value = self._convert_to_final_type(wire_values[0].value)

            if hasattr(final_value, '_set_parent'):
                final_value._set_parent((instance, self.__field_number, None))

            return final_value

    def __set__(self, instance, value):
        if not self._validate(value):
            raise ValueError

        instance._set_wire_values(self.__field_number, self.WIRE_TYPE, self._convert_to_wire_type(value))


