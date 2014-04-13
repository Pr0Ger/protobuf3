class BaseField(object):
    DEFAULT_VALUE = None

    def __init__(self, field_number=None, required=False, optional=False, repeated=False):
        assert isinstance(field_number, int)

        self.__field_number = field_number
        self.__required = required
        self.__optional = optional
        self.__repeated = repeated

    def _convert_to_final_type(self, value):
        return value

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
