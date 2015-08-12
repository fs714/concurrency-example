import threading
import logging
import Queue
import requests
import time

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

task_queue = Queue.Queue()


def async_call(func, callback, *args, **kwargs):
    task_queue.put({
        'function': func,
        'callback': callback,
        'args':     args,
        'kwargs':   kwargs
    })


def task_queue_consumer():
    while True:
        try:
            task = task_queue.get()
            func = task.get('function')
            callback = task.get('callback')
            args = task.get('args')
            kwargs = task.get('kwargs')
            try:
                if callback:
                    callback(func(*args, **kwargs))
            finally:
                task_queue.task_done()
        except Exception as ex:
            logging.warning(ex)


def get_url(url):
    return requests.get(url)


def print_response(res):
    logger.info(res.text)

if __name__ == '__main__':
    url = 'http://127.0.0.1/1'
    loop = 100
    worker_num = 10

    for i in xrange(worker_num):
        t = threading.Thread(target=task_queue_consumer)
        t.setDaemon(True)
        t.start()

    for i in xrange(loop):
        async_call(get_url, print_response, url)
        logger.info('async_call finish loop ' + str(i))

    task_queue.join()
