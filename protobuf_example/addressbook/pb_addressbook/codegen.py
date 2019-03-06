# Run this scripts in project root path

from grpc_tools import protoc

protoc.main((
    '',
    '--proto_path=.',
    '--proto_path=/usr/local/include/',
    '--python_out=.',
    './protobuf_example/addressbook/pb_addressbook/addressbook.proto',
))
