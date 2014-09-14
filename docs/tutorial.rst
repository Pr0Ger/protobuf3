Tutorial
========

This tutorial is intended as an introduction to working with **protobuf3**.

Prerequisites
-------------
Before we start, make sure that you have the **PyMongo** distribution :doc:`installed <installation>`.
In the Python shell, the following should run without raising an exception:

.. doctest::

  >>> import protobuf3

This tutorial also assumes that you have installed protobuf compiler. The following command should run
and show libprotobuf version:

.. code-block:: bash

  $ protoc --version

Defining your protocol format
-----------------------------

I don't want to copy-paste official protobuf tutorials, so if you want some explanation for this file,
you can find it `here <https://developers.google.com/protocol-buffers/docs/pythontutorial>`_.

.. code-block:: protobuf

    package tutorial;

    message Person {
      required string name = 1;
      required int32 id = 2;
      optional string email = 3;

      enum PhoneType {
        MOBILE = 0;
        HOME = 1;
        WORK = 2;
      }

      message PhoneNumber {
        required string number = 1;
        optional PhoneType type = 2 [default = HOME];
      }

      repeated PhoneNumber phone = 4;
    }

    message AddressBook {
      repeated Person person = 1;
    }

Compiling your protocol buffers
-------------------------------

It's very similar with original protobuf implementation. There is only one different thing: use
**--python3_out** instead of **--python_out**


Generated code example
----------------------

Protobuf compiler will generate this code for example .proto file

.. code-block:: python

    from protobuf3.message import Message
    from protobuf3.fields import StringField, EnumField, Int32Field, MessageField
    from enum import Enum


    class Person(Message):

        class PhoneType(Enum):
            MOBILE = 0
            HOME = 1
            WORK = 2

        class PhoneNumber(Message):
            pass


    class AddressBook(Message):
        pass

    Person.PhoneNumber.add_field('number', StringField(field_number=1, required=True))
    Person.PhoneNumber.add_field('type', EnumField(field_number=2, optional=True, enum_cls=Person.PhoneType, default=Person.PhoneType.HOME))
    Person.add_field('name', StringField(field_number=1, required=True))
    Person.add_field('id', Int32Field(field_number=2, required=True))
    Person.add_field('email', StringField(field_number=3, optional=True))
    Person.add_field('phone', MessageField(field_number=4, repeated=True, message_cls=Person.PhoneNumber))
    AddressBook.add_field('person', MessageField(field_number=1, repeated=True, message_cls=Person))


But this library also support django-style code for defining data model (this form is more readable).
Same code, but hand-written using this style:

.. code-block:: python

    from protobuf3.message import Message
    from protobuf3.fields import StringField, EnumField, Int32Field, MessageField
    from enum import Enum


    class Person(Message):

        class PhoneType(Enum):
            MOBILE = 0
            HOME = 1
            WORK = 2

        class PhoneNumber(Message):
            number = StringField(field_number=1, required=True)
            type = EnumField(field_number=2, optional=True, enum_cls=Person.PhoneType, default=Person.PhoneType.HOME)

        name = StringField(field_number=1, required=True)
        id = Int32Field(field_number=2, required=True)
        email = StringField(field_number=3, optional=True)
        phone = MessageField(field_number=4, repeated=True, message_cls=Person.PhoneNumber)


    class AddressBook(Message):
        person = MessageField(field_number=1, repeated=True, message_cls=Person)


The Protocol Buffer API
-----------------------

It's very similar to original implementation. Currently there is some difference how repeated field work
(probably I make some comparability changes).

.. doctest::
    >>> person = address.Person()
    >>> person.id = 1234
    >>> person.name = "John Doe"
    >>> person.email = "jdoe@example.com"
    >>> number = address.Person.PhoneNumber()
    >>> number.number = "123"
    >>> person.phone.append(number)

    >>> person.encode_to_bytes()
    b'\n\x08John Doe\x10\xd2\t\x1a\x10jdoe@example.com"\x05\n\x03123'

    >>> new_person = address.Person()
    >>> new_person.parse_from_bytes(b'\n\x08John Doe\x10\xd2\t\x1a\x10jdoe@example.com"\x05\n\x03123')
    >>> assert new_person.id == 1234
