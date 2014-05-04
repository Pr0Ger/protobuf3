from collections import namedtuple
from os.path import splitext
from protobuf3.compiler.plugin_api import FieldDescriptorProto

MessageCode = namedtuple('MessageCode', ['name', 'fields'])

field_labels = {
    FieldDescriptorProto.Label.LABEL_REQUIRED: "required=True",
    FieldDescriptorProto.Label.LABEL_OPTIONAL: "optional=True",
    FieldDescriptorProto.Label.LABEL_REPEATED: "repeated=True"
}

field_types = {
    FieldDescriptorProto.Type.TYPE_BOOL: 'BoolField',
    FieldDescriptorProto.Type.TYPE_BYTES: 'BytesField',
    FieldDescriptorProto.Type.TYPE_DOUBLE: 'DoubleField',
    # FieldDescriptorProto.Type.TYPE_ENUM: 'EnumField',
    FieldDescriptorProto.Type.TYPE_FIXED32: 'Fixed32Field',
    FieldDescriptorProto.Type.TYPE_FIXED64: 'Fixed64Field',
    FieldDescriptorProto.Type.TYPE_FLOAT: 'FloatField',
    FieldDescriptorProto.Type.TYPE_INT32: 'Int32Field',
    FieldDescriptorProto.Type.TYPE_INT64: 'Int64Field',
    # FieldDescriptorProto.Type.TYPE_MESSAGE: 'MessageField',
    FieldDescriptorProto.Type.TYPE_SFIXED32: 'SFixed32Field',
    FieldDescriptorProto.Type.TYPE_SFIXED64: 'SFixed64Field',
    FieldDescriptorProto.Type.TYPE_SINT32: 'SInt32Field',
    FieldDescriptorProto.Type.TYPE_SINT64: 'SInt64Field',
    FieldDescriptorProto.Type.TYPE_STRING: 'StringField',
    FieldDescriptorProto.Type.TYPE_UINT32: 'UInt32Field',
    FieldDescriptorProto.Type.TYPE_UINT64: 'UInt64Field'
}


class Compiler(object):
    def __init__(self, fdesc):
        self.__fdesc = fdesc
        self.__imports = {
            'protobuf3.message': {'Message'},
            'protobuf3.fields': set(),
        }

        self.__messages_code = []
        self.__fields_code = ['']

        for message in fdesc.message_type:
            self.process_message(message)

    def return_file_name(self):
        return splitext(self.__fdesc.name)[0] + '.py'

    def return_file_contents(self):
        imports = []

        for it in self.__imports:
            imports.append("from {} import {}".format(it, ', '.join(self.__imports[it])))

        self.__fields_code.append('')

        return '\n'.join(map(lambda x: '\n'.join(x), (imports, self.__messages_code, self.__fields_code)))

    def process_message(self, message):
        self.__messages_code.extend([
            "",
            "",
            "class {}(Message):".format(message.name),
            "    pass"
        ])

        for field in message.field:
            self.process_field(message.name, field)

    def process_field(self, msg_name, field):
        field_args = [
            "field_number=" + str(field.number),
            field_labels[field.label]
        ]

        field = {
            'msg': msg_name,
            'field_name': field.name,
            'field_type': field_types[field.type],
            'field_args': ', '.join(field_args),
        }

        self.__imports['protobuf3.fields'].add(field['field_type'])

        self.__fields_code.append("{msg}.add_field('{field_name}', {field_type}({field_args}))".format(**field))
