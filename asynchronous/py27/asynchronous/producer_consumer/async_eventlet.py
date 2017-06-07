import eventlet
from eventlet.green import urllib2
import logging

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


def consumer(task_queue):
    while True:
        next_task = task_queue.get()
        next_task()
        task_queue.task_done()


class Task(object):
    def __init__(self, url):
        self.url = url

    def __call__(self):
        res = urllib2.urlopen(self.url).read()
        logger.info('In green thread: ' + res)
        return res

if __name__ == '__main__':
    url = 'http://127.0.0.1/1'
    num_consumers = 10
    num_tasks = 100

    task_queue = eventlet.Queue()

    pool = eventlet.GreenPool()
    for i in xrange(num_consumers):
        pool.spawn(consumer, task_queue)

    for i in xrange(num_tasks):
        task_queue.put(Task(url))
        logger.info('async_call finish loop ' + str(i))

    task_queue.join()
