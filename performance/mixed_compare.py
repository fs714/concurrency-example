import logging
import multiprocessing
from multiprocessing.pool import ThreadPool
import threading
import time

logging.basicConfig()
logger = logging.getLogger("mixed_task_campare")
logger.setLevel(logging.DEBUG)

LOOP = 5000
NUM = 50000
elapsed_time = {}


def count(n):
    while n > 0:
        n = n - 1
    time.sleep(0.1)


# Sequential execution
# logger.info('Sequential execution')
# start = time.time()
# for i in xrange(LOOP):
#     count(NUM)
# stop = time.time()
# elapsed_time['Sequential'] = stop - start

# Threaded exeution
logger.info('Threaded exeution')
start = time.time()
threads = []
for i in xrange(LOOP):
    thread = threading.Thread(target=count, args=(NUM,))
    thread.start()
    threads.append(thread)
for t in threads:
    t.join()
stop = time.time()
elapsed_time['Threaded'] = stop - start

# Thread pool execution
logger.info('Thread pool execution')
start = time.time()
pool = ThreadPool(processes=200)
for i in xrange(LOOP):
    pool.apply_async(count, (NUM,))
pool.close()
pool.join()
stop = time.time()
elapsed_time['ThreadPool(200)'] = stop - start

# Processed exeution
logger.info('Processed exeution')
start = time.time()
processes = []
for i in xrange(LOOP):
    process = multiprocessing.Process(target=count, args=(NUM,))
    process.start()
    processes.append(process)
for p in processes:
    p.join()
stop = time.time()
elapsed_time['Processed'] = stop - start

# Multiprocessing pool execution
logger.info('Multiprocessing pool(200) execution')
start = time.time()
pool = multiprocessing.Pool(processes=200)
for i in xrange(LOOP):
    pool.apply_async(count, (NUM,))
pool.close()
pool.join()
stop = time.time()
elapsed_time['ProcessPool(200)'] = stop - start

# Multiprocessing pool plus thread pool execution
logger.info('Multiprocessing pool(2) plus thread pool(100) execution')

def threadpool_executor(processes=None, func=None, iterable=None):
    threadpool = ThreadPool(processes=processes)
    threadpool.map(func, iterable)

start = time.time()
cpus = multiprocessing.cpu_count()
pool = multiprocessing.Pool(processes=cpus)
for i in xrange(cpus):
    pool.apply_async(threadpool_executor, (100, count, [NUM] * (LOOP / cpus)))
pool.close()
pool.join()
stop = time.time()
elapsed_time['MultiProcessingPool(2)_ThreadPool(100)'] = stop - start

# Compare performance
for key, value in sorted(elapsed_time.iteritems()):
    logger.info("\t" + key + "\t" + str(value))
