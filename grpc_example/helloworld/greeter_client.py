import logging
from datetime import datetime

import grpc

from grpc_example.helloworld.pb_greeter import greeter_pb2, greeter_pb2_grpc


def run():
    with grpc.insecure_channel(
            target='localhost:50051',
            options=[
                ('grpc.lb_policy_name', 'round_robin'),
                ('grpc.enable_retries', 0),
                ('grpc.keepalive_timeout_ms', 10000)
            ]) as channel:
        stub = greeter_pb2_grpc.GreeterStub(channel)

        print(datetime.now().strftime("%H:%M:%S") + " Sync call")
        response = stub.SayHello(greeter_pb2.HelloRequest(name='you'), timeout=10)
        print(datetime.now().strftime("%H:%M:%S") + " Greeter client received: " + response.message)

        print(datetime.now().strftime("%H:%M:%S") + " Async call")
        response_future = stub.SayHello.future(greeter_pb2.HelloRequest(name='you'), timeout=10)
        print(datetime.now().strftime("%H:%M:%S") + " Async call finished")
        response = response_future.result()
        print(datetime.now().strftime("%H:%M:%S") + " Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()
