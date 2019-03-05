# Run this scripts in project root path

from grpc_tools import protoc

protoc.main((
    '',
    '--proto_path=.',
    '--python_out=.',
    './protobuf_example/proto/address_book.proto',
))
