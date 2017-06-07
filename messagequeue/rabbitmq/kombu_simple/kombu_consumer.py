import os
import logging
import multiprocessing
from kombu import Connection
from kombu.messaging import Consumer
from kombu_queues import task_json_queue, task_pickle_queue
from kombu_tasks import get_url_task

logging.basicConfig()
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.DEBUG)

rabbitmq_url = 'amqp://guest:guest@localhost:5672//'
worker_num = 100


def process_json(body, message):
    url = body['url']
    delay = body['delay']
    logger.info('Process JSON Message: ' + url + '/' + str(delay) + '/')
    get_url_task(url, delay)
    message.ack()


def process_pickle(body, message):
    func = body['func']
    args = body['args']
    kwargs = body['kwargs']
    try:
        func(*args, **kwargs)
    except Exception as ex:
        logger.error('task raised exception: %r', ex)
    message.ack()


def worker(mq_url):
    connection = Connection(mq_url)
    channel = connection.channel()
    consumer_json = Consumer(channel, task_json_queue,
                             callbacks=[process_json],
                             accept=['json'])
    consumer_json.consume()
    consumer_pickle = Consumer(channel, task_pickle_queue,
                               callbacks=[process_pickle],
                               accept=['pickle'])
    consumer_pickle.consume()
    while True:
        connection.drain_events()

if __name__ == '__main__':
    for i in xrange(worker_num):
        p = multiprocessing.Process(target=worker, args=(rabbitmq_url,))
        p.start()
