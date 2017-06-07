import multiprocessing
import requests
import logging

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


class Consumer(multiprocessing.Process):
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            logger.info(proc_name + ' --> ' + next_task.__str__())
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)


class Task(object):
    def __init__(self, url):
        self.url = url

    def __call__(self):
        res = requests.get(self.url).text
        logger.info('In process: ' + res)
        return res

    def __str__(self):
        return 'Get url ' + self.url

if __name__ == '__main__':
    url = 'http://127.0.0.1/1'
    num_consumers = 10
    num_tasks = 100

    task_queue = multiprocessing.JoinableQueue()
    result_queue = multiprocessing.Queue()

    for i in xrange(num_consumers):
        consumer = Consumer(task_queue, result_queue)
        consumer.daemon = True
        consumer.start()

    for i in xrange(num_tasks):
        task_queue.put(Task(url))
        logger.info('async_call finish loop ' + str(i))

    task_queue.join()

    for i in xrange(num_tasks):
        logger.info('Result: ' + result_queue.get())
