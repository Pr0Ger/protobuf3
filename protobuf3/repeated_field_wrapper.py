class RepeatedFieldWrapper(object):
    def __init__(self, message, field_number):
        self.__message = message
        self.__field_number = field_number
