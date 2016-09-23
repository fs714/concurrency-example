import multiprocessing
import threading
import time


def task(q):
    while True:
        if not q.empty():
            value = q.get(False)
            print('Get {} from queue'.format(value))
            time.sleep(1)
        else:
            break


def thread_executor(workers=None, func=None, task_queue=None):
    threads = []
    for i in xrange(workers):
        thread = threading.Thread(target=func, args=(task_queue,))
        thread.start()
        threads.append(thread)
    for t in threads:
        t.join()


if __name__ == '__main__':

    manager = multiprocessing.Manager()
    task_queue = manager.Queue()

    for i in xrange(1000):
        task_queue.put('task_' + str(i))

    cpus = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cpus)
    for i in xrange(cpus):
        pool.apply_async(thread_executor, (100, task, task_queue))
    pool.close()
    pool.join()
