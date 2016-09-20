import threading
import multiprocessing
import time
import logging


logging.basicConfig()
logger = logging.getLogger("thread_is_slow")
logger.setLevel(logging.DEBUG)

LOOP = 50
NUM = 10000000
elapsed_time = {}


def count(n):
    while n > 0:
        n = n - 1

# Sequential execution
logger.info('Sequential execution')
start = time.time()
for i in xrange(LOOP):
    count(NUM)
stop = time.time()
elapsed_time['Sequential'] = stop - start

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
logger.info('Multiprocessing pool execution')
start = time.time()
pool = multiprocessing.Pool(processes=2)
for i in xrange(LOOP):
    pool.apply_async(count, (NUM, ))
pool.close()
pool.join()
stop = time.time()
elapsed_time['ProcessPool(2)'] = stop - start

logger.info('Multiprocessing pool(4) execution')
start = time.time()
pool = multiprocessing.Pool(processes=4)
for i in xrange(LOOP):
    pool.apply_async(count, (NUM, ))
pool.close()
pool.join()
stop = time.time()
elapsed_time['ProcessPool(4)'] = stop - start

logger.info('Multiprocessing pool(8) execution')
start = time.time()
pool = multiprocessing.Pool(processes=8)
for i in xrange(LOOP):
    pool.apply_async(count, (NUM, ))
pool.close()
pool.join()
stop = time.time()
elapsed_time['ProcessPool(8)'] = stop - start

logger.info('Multiprocessing pool(16) execution')
start = time.time()
pool = multiprocessing.Pool(processes=16)
for i in xrange(LOOP):
    pool.apply_async(count, (NUM, ))
pool.close()
pool.join()
stop = time.time()
elapsed_time['ProcessPool(16)'] = stop - start


# Compare performance
for key, value in sorted(elapsed_time.iteritems()):
    logger.info("\t" + key + "\t" + str(value))
