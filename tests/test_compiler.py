from enum import Enum
from importlib.machinery import SourceFileLoader
from os import environ, path
from subprocess import Popen
from tempfile import NamedTemporaryFile, TemporaryDirectory
from unittest import TestCase


class TestCompiler(TestCase):
    def run_protoc_compiler(self, proto_code):
        self.proto_file = NamedTemporaryFile(suffix='.proto')
        self.out_dir = TemporaryDirectory()

        self.proto_file.write(proto_code.encode())
        self.proto_file.flush()

        new_env = environ.copy()
        new_env['PATH'] += ':' + path.normpath(path.join(path.dirname(__file__), '..', 'bin'))
        if 'PYTHONPATH' in new_env:
            new_env['PYTHONPATH'] += ':' + path.normpath(path.join(path.dirname(__file__), '..'))
        else:
            new_env['PYTHONPATH'] = path.normpath(path.join(path.dirname(__file__), '..'))

        args = [
            'protoc',
            '--python3_out=' + self.out_dir.name,
            '--proto_path=' + path.dirname(self.proto_file.name),
            self.proto_file.name
        ]
        proc = Popen(args, env=new_env)
        proc.wait()

        assert proc.returncode == 0

        filename, ext = path.splitext(path.basename(self.proto_file.name))
        generated_file = path.join(self.out_dir.name, filename + '.py')

        loader = SourceFileLoader("generated_files", generated_file)
        foo = loader.load_module("generated_files")

        self.proto_file.close()
        self.out_dir.cleanup()

        return foo

    def test_simple_fields(self):
        msg_code = '''
        message TestMsg {
            optional bool a = 1;
            optional string b = 2;
        }'''

        msgs = self.run_protoc_compiler(msg_code)

        msg = msgs.TestMsg()
        msg.parse_from_bytes(b'\x08\x01\x12\x07\x74\x65\x73\x74\x69\x6E\x67')
        self.assertEqual(msg.a, True)
        self.assertEqual(msg.b, 'testing')

    def test_embedded_messages(self):
        msg_code = '''
        message TestA {
            message Foo {
                optional int32 a = 1;
            }

            optional Foo b = 3;
        }

        message Bar {
            optional int32 a = 1;
        }

        message TestB {
            optional Bar b = 3;
        }

        message TestC {
            optional TestA.Foo b = 3;
        }'''

        msgs = self.run_protoc_compiler(msg_code)

        self.assertEqual(type(msgs.TestA.Foo), type)

        msgA = msgs.TestA()
        msgA.parse_from_bytes(b'\x1a\x03\x08\x96\x01')
        self.assertEqual(msgA.b.a, 150)

        msgB = msgs.TestB()
        msgB.parse_from_bytes(b'\x1a\x03\x08\x96\x01')
        self.assertEqual(msgB.b.a, 150)

        msgC = msgs.TestC()
        msgC.parse_from_bytes(b'\x1a\x03\x08\x96\x01')
        self.assertEqual(msgC.b.a, 150)

    def test_enums(self):
        msg_code = '''
        message TestA {
            enum Foo {
                Opt1 = 1;
                Opt2 = 2;
                Opt3 = 3;
            }
            optional Foo a = 1;
        }

        enum Bar {
            Opt1 = 1;
            Opt2 = 2;
        }

        message TestB {
            optional Bar a = 1;
        }'''

        msgs = self.run_protoc_compiler(msg_code)

        self.assertTrue(isinstance(msgs.TestA.Foo, type))
        self.assertTrue(issubclass(msgs.TestA.Foo, Enum))

        msg_a = msgs.TestA()
        msg_a.parse_from_bytes(b'\x08\x02')
        self.assertEqual(msg_a.a, msgs.TestA.Foo.Opt2)

        msg_b = msgs.TestB()
        msg_b.parse_from_bytes(b'\x08\x02')
        self.assertEqual(msg_b.a, msgs.Bar.Opt2)

    def test_default_option(self):
        msg_code = '''
        enum Foo {
            Opt1 = 1;
            Opt2 = 2;
        }

        message TestA {
            optional bool a = 1 [default = true];
            optional string b = 2 [default = 'asd'];
            optional bytes c = 3 [default = 'q\x08e'];
            optional Foo d = 4 [default = Opt2];
            optional int32 e = 5 [default = 1];
        }'''

        msgs = self.run_protoc_compiler(msg_code)

        msg_a = msgs.TestA()

        self.assertEqual(msg_a.a, True)
        self.assertEqual(msg_a.b, 'asd')
        self.assertEqual(msg_a.c, b'q\x08e')
        self.assertEqual(msg_a.d, msgs.Foo.Opt2)
        self.assertEqual(msg_a.e, 1)

    def test_message_without_fields(self):
        msg_code = '''
        message Foo {
        }'''

        self.run_protoc_compiler(msg_code)

    def test_enum_alias(self):
        msg_code = '''
        enum EnumAllowingAlias {
            option allow_alias = true;
            UNKNOWN = 0;
            STARTED = 1;
            RUNNING = 1;
        }'''

        # Compile without warnings
        self.run_protoc_compiler(msg_code)

        msg_code = '''
        enum EnumNotAllowingAlias {
            UNKNOWN = 0;
            STARTED = 1;
            RUNNING = 1;
        }'''

        # Protoc will return warning, but compile this code
        self.run_protoc_compiler(msg_code)

        msg_code = '''
        enum EnumForciblyNotAllowingAlias {
            option allow_alias = false;
            UNKNOWN = 0;
            STARTED = 1;
            RUNNING = 1;
        }'''

        # Protoc will crash with non-zero return code
        self.assertRaises(AssertionError, self.run_protoc_compiler, msg_code)

    def test_extend_message(self):
        msg_code = '''
        message Foo {
            message Bar {
                extensions 100 to 199;
            }

            extend Foo {
                optional int32 test = 104;
            }

            extensions 100 to 199;
        }

        extend Foo {
            optional int32 foo = 101;
        }

        extend Foo.Bar {
            optional int32 bar = 102;
        }'''

        msgs = self.run_protoc_compiler(msg_code)

        msg_foo = msgs.Foo()
        msg_foo.parse_from_bytes(b'\xa8\x06{\xc0\x06\x95\x06')

        self.assertTrue(hasattr(msg_foo, 'foo'))
        self.assertEqual(msg_foo.foo, 123)

        self.assertTrue(hasattr(msg_foo, 'test'))
        self.assertEqual(msg_foo.test, 789)


        msg_bar = msgs.Foo.Bar()
        msg_bar.parse_from_bytes(b'\xb0\x06\xc8\x03')
        self.assertTrue(hasattr(msg_bar, 'bar'))
        self.assertEqual(msg_bar.bar, 456)
