class RepeatedFieldWrapper(object):
    def __init__(self, message, field_number):
        self.__message = message
        self.__field_number = field_number

    def __len__(self):
        return len(self.__message._get_wire_values(self.__field_number))
