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

        self._instance = None  # Some kind of dirty hack for list access methods, will be assigned in __get__

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
        self._instance = instance  # some functions should know it, but only __get__ receive it as parameter

        wire_values = instance._get_wire_values(self.__field_number)

        final_values = [self._convert_to_final_type(it.value) for it in wire_values]

        if not final_values:
            final_values.append(self.default_value)

        if self.__repeated:
            return self
        else:
            final_values = final_values[0]
            return final_values

    def __getitem__(self, item):
        assert self.__repeated

        if isinstance(item, slice):
            raise NotImplementedError

        wire_value = self._instance._get_wire_values(self.__field_number)[item]

        return self._convert_to_final_type(wire_value.value)

    def __setitem__(self, key, value):
        if not self._validate(value):
            raise ValueError

        self._instance._set_wire_values(self.__field_number, self.WIRE_TYPE, self._convert_to_wire_type(value), key)

    def __set__(self, instance, value):
        if not self._validate(value):
            raise ValueError

        instance._set_wire_values(self.__field_number, self.WIRE_TYPE, self._convert_to_wire_type(value))

    def __len__(self):
        assert self._instance

        if self.__repeated:
            return len(self._instance._get_wire_values(self.__field_number))
        else:
            raise TypeError("Using len() isn't allowed for not repeated fields")

    def append(self, value):
        assert self._instance

        self._instance._set_wire_values(self.__field_number, self.WIRE_TYPE, self._convert_to_wire_type(value),
                                         append=True)

    def insert(self, index, value):
        assert self._instance

        self._instance._set_wire_values(self.__field_number, self.WIRE_TYPE, self._convert_to_wire_type(value),
                                         index=index, insert=True)
