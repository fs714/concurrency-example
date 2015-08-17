from kombu.pools import producers
from kombu_queues import task_exchange

priority_to_routing_key = {'high': 'hipri',
                           'mid': 'midpri',
                           'low': 'lopri'}

def send_task(connection, func, args=(), kwargs={}, priority='mid'):
    pay_load = {'func': func, 'args': args, 'kwargs': kwargs}
    routing_key = priority_to_routing_key[priority]

    with producers[connection].acquire(block=True) as producer:
        producer.publish(pay_load,
                         serializer='pickle',
                         compression='bzip2',
                         exchange=task_exchange,
                         declare=[task_exchange],
                         routing_key=routing_key)

if __name__ == '__main__':
    from kombu import Connection
    from kombu_tasks import hello_task

    connection = Connection('amqp://guest:guest@localhost:5672//')
    for i in xrange(10):
        send_task(connection, hello_task, args=('Kombu High', ), kwargs={}, priority='high')
        send_task(connection, hello_task, args=('Kombu Middle', ), kwargs={}, priority='mid')
        send_task(connection, hello_task, args=('Kombu Low', ), kwargs={}, priority='low')
