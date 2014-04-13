class BaseField(object):
    DEFAULT_VALUE = None
    WIRE_TYPE = -1

    def __init__(self, field_number=None, required=False, optional=False, repeated=False):
        assert isinstance(field_number, int)

        if repeated:
            raise NotImplementedError("Repeated fields doesn't supported yet")

        self.__field_number = field_number
        self.__required = required
        self.__optional = optional
        self.__repeated = repeated

    def _convert_to_final_type(self, value):
        return value

    def _convert_to_wire_type(self, value):
        return value

    def _validate(self, value):
        return True

    def __get__(self, instance, owner):
        wire_values = instance._get_wire_values(self.__field_number)

        final_values = [self._convert_to_final_type(it.value) for it in wire_values]

        if not final_values:
            final_values.append(self.__class__.DEFAULT_VALUE)

        if not self.__repeated:
            final_values = final_values[0]
        else:
            pass
            # TODO: implement support for repeated values
        return final_values

    def __set__(self, instance, value):
        if not self._validate(value):
            raise ValueError

        instance._set_wire_values(self.__field_number, self.WIRE_TYPE, self._convert_to_wire_type(value))
