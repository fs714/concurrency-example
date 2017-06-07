from kombu import Connection
from kombu.messaging import Producer
from kombu.transport.base import Message
from kombu_queues import task_exchange
from kombu_tasks import echo_task

rabbitmq_url = 'amqp://guest:guest@localhost:5672//'
message_num = 400

if __name__ == '__main__':
    connection = Connection(rabbitmq_url)
    channel = connection.channel()

    body_json = {'url': 'http://127.0.0.1',
                 'delay': 5}
    message_json = Message(channel, body=body_json)

    body_pickle = {'func': echo_task,
                   'args': ('Hello Rabbit', 5),
                   'kwargs': {}}
    message_pickle = Message(channel, body=body_pickle)

    producer_json = Producer(channel, exchange=task_exchange)
    producer_pickle = Producer(channel, exchange=task_exchange, serializer='pickle')
    for i in xrange(message_num):
        producer_json.publish(message_json.body, routing_key='json_queue')
        producer_pickle.publish(message_pickle.body, routing_key='pickle_queue')
