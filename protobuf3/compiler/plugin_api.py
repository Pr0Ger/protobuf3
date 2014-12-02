from enum import Enum
from protobuf3.fields import *
from protobuf3.message import Message


class UninterpretedOption(Message):
    class NamePart(Message):
        name_part = StringField(field_number=1, required=True)
        is_extension = BoolField(field_number=2, required=True)

    name = MessageField(field_number=2, repeated=True, message_cls=NamePart)

    identifier_value = StringField(field_number=3, optional=True)
    positive_int_value = UInt64Field(field_number=4, optional=True)
    negative_int_value = Int64Field(field_number=5, optional=True)
    double_value = DoubleField(field_number=6, optional=True)
    string_value = BytesField(field_number=7, optional=True)
    aggregate_value = StringField(field_number=8, optional=True)


class MessageOptions(Message):
    message_set_wire_format = BoolField(field_number=1, optional=True)
    no_standard_descriptor_accessor = BoolField(field_number=2, optional=True)
    deprecated = BoolField(field_number=3, optional=True, default=False)
    map_entry = BoolField(field_number=7, optional=True)
    uninterpreted_option = MessageField(field_number=999, repeated=True,
                                        message_cls=UninterpretedOption)


class EnumOptions(Message):
    allow_alias = BoolField(field_number=2, optional=True, default=True)
    deprecated = BoolField(field_number=3, optional=True, default=False)
    uninterpreted_option = MessageField(field_number=999, repeated=True,
                                        message_cls=UninterpretedOption)


class MethodOptions(Message):
    deprecated = BoolField(field_number=33, optional=True, default=False)
    uninterpreted_option = MessageField(field_number=999, repeated=True,
                                        message_cls=UninterpretedOption)


class ServiceOptions(Message):
    deprecated = BoolField(field_number=33, optional=True, default=False)
    uninterpreted_option = MessageField(field_number=999, repeated=True,
                                        message_cls=UninterpretedOption)


class EnumValueOptions(Message):
    deprecated = BoolField(field_number=1, optional=True, default=False)
    uninterpreted_option = MessageField(field_number=999, repeated=True,
                                        message_cls=UninterpretedOption)


class OneofDescriptorProto(Message):
    name = StringField(field_number=1, optional=True)


class FieldOptions(Message):
    class CType(Enum):
        STRING = 0
        CORD = 1
        STRING_PIECE = 2

    ctype = EnumField(field_number=1, optional=True, enum_cls=CType, default=CType.STRING)
    packed = BoolField(field_number=2, optional=True)
    lazy = BoolField(field_number=5, optional=True)
    deprecated = BoolField(field_number=3, optional=True)
    experimental_map_key = StringField(field_number=9, optional=True)
    weak = BoolField(field_number=10, optional=True)

    uninterpreted_option = MessageField(field_number=999, message_cls=UninterpretedOption)


class FieldDescriptorProto(Message):
    class Type(Enum):
        TYPE_DOUBLE = 1
        TYPE_FLOAT = 2
        TYPE_INT64 = 3
        TYPE_UINT64 = 4
        TYPE_INT32 = 5
        TYPE_FIXED64 = 6
        TYPE_FIXED32 = 7
        TYPE_BOOL = 8
        TYPE_STRING = 9
        TYPE_GROUP = 10
        TYPE_MESSAGE = 11
        TYPE_BYTES = 12
        TYPE_UINT32 = 13
        TYPE_ENUM = 14
        TYPE_SFIXED32 = 15
        TYPE_SFIXED64 = 16
        TYPE_SINT32 = 17
        TYPE_SINT64 = 18

    class Label(Enum):
        LABEL_OPTIONAL = 1
        LABEL_REQUIRED = 2
        LABEL_REPEATED = 3

    name = StringField(field_number=1, optional=True)
    number = Int32Field(field_number=3, optional=True)
    label = EnumField(field_number=4, optional=True, enum_cls=Label)

    type = EnumField(field_number=5, optional=True, enum_cls=Type)

    type_name = StringField(field_number=6, optional=True)

    extendee = StringField(field_number=2, optional=True)

    default_value = StringField(field_number=7, optional=True)

    options = MessageField(field_number=8, message_cls=FieldOptions)

    oneof_index = Int32Field(field_number=9, optional=True)


class EnumValueDescriptorProto(Message):
    name = StringField(field_number=1, optional=True)
    number = Int32Field(field_number=2, optional=True)

    options = MessageField(field_number=3, optional=True, message_cls=EnumValueOptions)


class EnumDescriptorProto(Message):
    name = StringField(field_number=1, optional=True)
    value = MessageField(field_number=2, repeated=True, message_cls=EnumValueDescriptorProto)

    options = MessageField(field_number=3, optional=True, message_cls=EnumOptions)


class DescriptorProto(Message):
    name = StringField(field_number=1, optional=True)

    field = MessageField(field_number=2, repeated=True, message_cls=FieldDescriptorProto)
    extension = MessageField(field_number=6, repeated=True, message_cls=FieldDescriptorProto)

    enum_type = MessageField(field_number=4, repeated=True, message_cls=EnumDescriptorProto)

    class ExtensionRange(Message):
        start = Int32Field(field_number=1, optional=True)
        end = Int32Field(field_number=2, optional=True)

    extension_range = MessageField(field_number=5, repeated=True, message_cls=ExtensionRange)

    options = MessageField(field_number=7, optional=True, message_cls=MessageOptions)

    oneof_decl = MessageField(field_number=8, repeated=True, message_cls=OneofDescriptorProto)


DescriptorProto.add_field('nested_type',
                          MessageField(field_number=3, repeated=True, message_cls=DescriptorProto))


class MethodDescriptorProto(Message):
    name = StringField(field_number=1, optional=True)

    input_type = StringField(field_number=2, optional=True)
    output_type = StringField(field_number=3, optional=True)

    options = MessageField(field_number=4, optional=True, message_cls=MethodOptions)

    client_streaming = BoolField(field_number=5, optional=True, default=False)
    server_streaming = BoolField(field_number=6, optional=True, default=False)


class ServiceDescriptorProto(Message):
    name = StringField(field_number=1, optional=True)
    method = MessageField(field_number=2, repeated=True, message_cls=MethodDescriptorProto)

    options = MessageField(field_number=3, optional=True, message_cls=ServiceOptions)


class FileOptions(Message):
    java_package = StringField(field_number=1, optional=True)

    java_outer_classname = StringField(field_number=8, optional=True)

    java_multiple_files = BoolField(field_number=10, optional=True)

    java_generate_equals_and_hash = BoolField(field_number=20, optional=True)

    class OptimizeMode(Enum):
        SPEED = 1
        CODE_SIZE = 2
        LITE_RUNTIME = 3

    optimize_for = EnumField(field_number=9, optional=True, enum_cls=OptimizeMode,
                             default=OptimizeMode.SPEED)

    go_package = StringField(field_number=11, optional=True)

    cc_generic_services = BoolField(field_number=16, optional=True)
    java_generic_services = BoolField(field_number=17, optional=True)
    py_generic_services = BoolField(field_number=18, optional=True)

    deprecated = BoolField(field_number=23, optional=True, default=False)

    uninterpreted_option = MessageField(field_number=999, repeated=True,
                                        message_cls=UninterpretedOption)


class FileDescriptorProto(Message):
    name = StringField(field_number=1, optional=True)
    package = StringField(field_number=2, optional=True)

    dependency = StringField(field_number=3, repeated=True)
    public_dependency = Int32Field(field_number=10, repeated=True)
    weak_dependency = Int32Field(field_number=11, repeated=True)  # Google-internal

    message_type = MessageField(field_number=4, repeated=True, message_cls=DescriptorProto)
    enum_type = MessageField(field_number=5, repeated=True, message_cls=EnumDescriptorProto)
    service = MessageField(field_number=6, repeated=True, message_cls=ServiceDescriptorProto)
    extension = MessageField(field_number=7, repeated=True, message_cls=FieldDescriptorProto)

    options = MessageField(field_number=8, optional=True, message_cls=FileOptions)

    # optional SourceCodeInfo source_code_info = 9;

    syntax = StringField(field_number=12, optional=True)


class CodeGeneratorRequest(Message):
    file_to_generate = StringField(field_number=1, repeated=True)
    parameter = StringField(field_number=2, optional=True)
    proto_file = MessageField(field_number=15, repeated=True, message_cls=FileDescriptorProto)


class CodeGeneratorResponse(Message):
    error = StringField(field_number=1, optional=True)

    class File(Message):
        name = StringField(field_number=1, optional=True)
        insertion_point = StringField(field_number=2, optional=True)
        content = StringField(field_number=15, optional=True)

    file = MessageField(field_number=15, repeated=True, message_cls=File)
