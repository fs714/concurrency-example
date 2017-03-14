import logging
from kombu.mixins import ConsumerMixin
from kombu.utils import kwdict, reprcall
from kombu_queues import task_queues


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Worker(ConsumerMixin):
    def __init__(self, connection):
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=task_queues,
                         accept=['pickle', 'json'],
                         callbacks=[self.process_task])]

    def process_task(self, body, message):
        func = body['func']
        args = body['args']
        kwargs = body['kwargs']
        logger.info('Got task: %s', reprcall(func.__name__, args, kwargs))
        try:
            func(*args, **kwdict(kwargs))
        except Exception as ex:
            logger.error('task raised exception: %r', ex)
        message.ack()

if __name__ == '__main__':
    from kombu import Connection
    import multiprocessing

    with Connection('amqp://guest:guest@localhost:5672//') as conn:
        for i in xrange(100):
            worker = Worker(conn)
            p = multiprocessing.Process(target=worker.run)
            p.start()
            logger.info('Worker ' + str(i) + ' started')
