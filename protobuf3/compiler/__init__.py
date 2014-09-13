from collections import namedtuple
from itertools import chain
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
    FieldDescriptorProto.Type.TYPE_ENUM: 'EnumField',
    FieldDescriptorProto.Type.TYPE_FIXED32: 'Fixed32Field',
    FieldDescriptorProto.Type.TYPE_FIXED64: 'Fixed64Field',
    FieldDescriptorProto.Type.TYPE_FLOAT: 'FloatField',
    FieldDescriptorProto.Type.TYPE_INT32: 'Int32Field',
    FieldDescriptorProto.Type.TYPE_INT64: 'Int64Field',
    FieldDescriptorProto.Type.TYPE_MESSAGE: 'MessageField',
    FieldDescriptorProto.Type.TYPE_SFIXED32: 'SFixed32Field',
    FieldDescriptorProto.Type.TYPE_SFIXED64: 'SFixed64Field',
    FieldDescriptorProto.Type.TYPE_SINT32: 'SInt32Field',
    FieldDescriptorProto.Type.TYPE_SINT64: 'SInt64Field',
    FieldDescriptorProto.Type.TYPE_STRING: 'StringField',
    FieldDescriptorProto.Type.TYPE_UINT32: 'UInt32Field',
    FieldDescriptorProto.Type.TYPE_UINT64: 'UInt64Field'
}


class Compiler(object):
    def __init__(self, fdesc, tle_map):
        self.__fdesc = fdesc
        self.__tle_map = tle_map

        self.__top_level_elements = []
        self.__imports = {
            'protobuf3.message': {'Message'},
            'protobuf3.fields': set(),
        }

        self.__messages_code = []
        self.__fields_code = ['']

        # This list should be completely built before start generating code
        for item in chain(fdesc.message_type, fdesc.enum_type):
            self.__top_level_elements.append(item.name)

        for message in fdesc.message_type:
            self.process_message(message)

        for enum in fdesc.enum_type:
            self.process_enum(enum)

        for ext in fdesc.extension:
            self.process_field(ext.extendee[1:], ext)

    def return_file_name(self):
        return splitext(self.__fdesc.name)[0] + '.py'

    def return_file_contents(self):
        imports = []

        for it in self.__imports:
            if self.__imports[it]:
                imports.append("from {} import {}".format(it, ', '.join(self.__imports[it])))

        self.__fields_code.append('')

        return '\n'.join(
            map(lambda x: '\n'.join(x), (imports, self.__messages_code, self.__fields_code)))

    def process_message(self, message, embedded=''):
        _empty = True

        indent = embedded.count('.') * '    '

        self.__messages_code.append('')
        if not embedded:
            # Two blank lines between top-level definitions
            self.__messages_code.append('')

        self.__messages_code.append(indent + "class {}(Message):".format(message.name))

        for enum in message.enum_type:
            _empty = False
            self.process_enum(enum, embedded + message.name + '.')

        for ext in message.extension:
            self.process_field(ext.extendee[1:], ext)

        for msg in message.nested_type:
            _empty = False
            self.process_message(msg, embedded + message.name + '.')

        if _empty:
            self.__messages_code.append(indent + '    pass')

        for field in message.field:
            self.process_field(message.name, field, embedded)

    def process_enum(self, enum, embedded=''):
        if 'enum' not in self.__imports:
            self.__imports['enum'] = {'Enum'}
        else:
            self.__imports['enum'].add('Enum')

        indent = embedded.count('.') * '    '

        self.__messages_code.append('')
        if not embedded:
            # Two blank lines between top-level definitions
            self.__messages_code.append('')

        if not enum.options.allow_alias:
            self.__imports['enum'].add('unique')
            self.__messages_code.append(indent + "@unique")

        self.__messages_code.append(indent + "class {}(Enum):".format(enum.name))

        for option in enum.value:
            self.__messages_code.append(indent + "    {} = {}".format(option.name, option.number))

    def process_field(self, msg_name, field, embedded=''):
        field_args = [
            "field_number=" + str(field.number),
            field_labels[field.label]
        ]

        type_name = None
        if field.type == FieldDescriptorProto.Type.TYPE_MESSAGE:
            type_name = self.__strip_package_name(field.type_name[1:])
            field_args.append("message_cls=" + type_name)

        if field.type == FieldDescriptorProto.Type.TYPE_ENUM:
            type_name = self.__strip_package_name(field.type_name[1:])
            field_args.append("enum_cls=" + type_name)

        if type_name:
            # Because we can have reference to something in other class, like Foo.Bar
            top_level_name = type_name.split('.')[0]

            if top_level_name not in self.__top_level_elements:
                file_to_import = splitext(self.__tle_map[top_level_name])[0].replace('/', '.')
                if file_to_import not in self.__imports:
                    self.__imports[file_to_import] = {top_level_name}
                else:
                    self.__imports[file_to_import].add(top_level_name)

        if 'default_value' in field:
            if field.type == FieldDescriptorProto.Type.TYPE_BOOL:
                default = field.default_value.title()
            elif field.type == FieldDescriptorProto.Type.TYPE_STRING:
                default = '"' + field.default_value + '"'
            elif field.type == FieldDescriptorProto.Type.TYPE_BYTES:
                default = "b'" + field.default_value + "'"
            elif field.type == FieldDescriptorProto.Type.TYPE_ENUM:
                default = type_name + '.' + field.default_value
            else:
                default = field.default_value

            field_args.append("default=" + default)

        field = {
            'msg': embedded + msg_name,
            'field_name': field.name,
            'field_type': field_types[field.type],
            'field_args': ', '.join(field_args),
        }

        self.__imports['protobuf3.fields'].add(field['field_type'])

        self.__fields_code.append(
            "{msg}.add_field('{field_name}', {field_type}({field_args}))".format(**field))

    def __strip_package_name(self, type_name):
        names = type_name.split('.')

        if names[0] == self.__fdesc.package:
            return '.'.join(names[1:])
        else:
            return type_name
