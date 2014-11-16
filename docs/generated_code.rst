Generated code explanation
==========================

This page describes exactly what Python definitions the protocol buffer compiler generates for any
given protocol definition. Also, this page is very similar to `same page <https://developers.google.com/protocol-buffers/docs/reference/python-generated>`_
from original implementation, so I describe only differences from original implementation.

Compiler invocation
-------------------

There is two significant differences:

#. **--python3_out** instead of **--python_out**.

#. There is no **_pb2** suffix in generated file names.

Messages
--------

Message can be loaded from serialized form two ways:

#. By calling class-method **create_from_bytes**
#. By creating instance and then calling instance method **parse_from_bytes**

And can be serialized by calling **encode_to_bytes**

Fields
------

Instead of original implementation, this one doesn't generate any constants with field numbers.

Singular fields
~~~~~~~~~~~~~~~

All works very similar to original implementation:

.. code-block:: python

    message.foo = 123
    print message.foo

There is some difference how you check fields presence:

.. code-block:: python

    assert not 'foo' in message
    message.foo = 123
    assert 'foo' in message

Also, currently there is no way for removing field (look at `PB3-23 <http://youtrack.pr0ger.org/issue/PB3-26>`_)

Singular Message Fields
~~~~~~~~~~~~~~~~~~~~~~~

There is no difference with original implementation

.. code-block:: protobuf

    message Foo {
        optional Bar bar = 1;
    }
    message Bar {
        optional int32 i = 1;
    }

.. code-block:: python

    foo = Foo()
    assert not 'bar' in foo
    foo.bar.i = 1
    assert 'bar' in foo
    assert foo.bar.i == 1

Repeated Fields
~~~~~~~~~~~~~~~

I copied this section from original documentation, but commented some lines, that currently not implemented:

#. `.extend() <http://youtrack.pr0ger.org/issue/PB3-27>`_

.. code-block:: protobuf

    message Foo {
        repeated int32 nums = 1;
    }

.. code-block:: python

    foo = Foo()
    foo.nums.append(15)        # Appends one value
    #foo.nums.extend([32, 47]) # Appends an entire list

    assert len(foo.nums) == 3
    assert foo.nums[0] == 15
    assert foo.nums[1] == 32
    #assert foo.nums == [15, 32, 47]

    foo.nums[1] = 56    # Reassigns a value
    assert foo.nums[1] == 56
    for i in foo.nums:  # Loops and print
      print i
    #del foo.nums[:]    # Clears list (works just like in a Python list)

Repeated Message Fields
~~~~~~~~~~~~~~~~~~~~~~~

It's very similar to original implementation. Currently **.add()** isn't `supported <http://youtrack.pr0ger.org/issue/PB3-23>`_

Enumerations
------------

In Python 3.4 default **enum** is used, for previous Python version this implementation will require
backported implementation `enum34 <https://pypi.python.org/pypi/enum34>`_.

Some example:

.. code-block:: protobuf

    message Foo {
        enum SomeEnum {
            VALUE_A = 1;
            VALUE_B = 5;
            VALUE_C = 1234;
        }
        optional SomeEnum bar = 1;
    }

After generating you will receive following code:

.. code-block:: python

    from enum import Enum
    from protobuf3.message import Message
    from protobuf3.fields import EnumField


    class Foo(Message):

        class SomeEnum(Enum):
            VALUE_A = 1
            VALUE_B = 5
            VALUE_C = 1234

    Foo.add_field('bar', EnumField(field_number=1, optional=True, enum_cls=Foo.SomeEnum))

And how this works:

.. code-block:: python

    foo = Foo()
    foo.bar = Foo.SomeEnum.VALUE_A
    assert foo.bar.value == 1
    assert foo.bar == Foo.SomeEnum.VALUE_A


Oneof
-----

`Not supported yet <http://youtrack.pr0ger.org/issue/PB3-20>`_.

Extensions
----------

Messages with extension works very similar to messages without extensions. Look at this sample:

.. code-block:: protobuf

    message Foo {
        extensions 100 to 199;
    }

    extend Foo {
        optional int32 bar = 123;
    }

.. code-block:: python

    from protobuf3.fields import Int32Field
    from protobuf3.message import Message


    class Foo(Message):
        pass

    Foo.add_field('bar', Int32Field(field_number=123, optional=True))

This should work even if message and extension declared in different files

