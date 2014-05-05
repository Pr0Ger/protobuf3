from importlib.machinery import SourceFileLoader
from os import environ, path
from subprocess import Popen, PIPE
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
        proc = Popen(args, stdout=PIPE, stderr=PIPE, env=new_env)
        proc.wait()

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
