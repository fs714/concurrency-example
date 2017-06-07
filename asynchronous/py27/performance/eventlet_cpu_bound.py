import eventlet
import logging
import time

eventlet.patcher.monkey_patch(all=True)

logging.basicConfig()
logger = logging.getLogger('eventlet')
logger.setLevel(logging.DEBUG)

LOOP = 50
green_thread_num = 10
process_num = 5
NUM = 10000000
elapsed_time = {}


def count(n):
    while n > 0:
        n = n - 1

# Only eventlet
logger.info('Eventlet execution')
start = time.time()
pool = eventlet.GreenPool(200)
for i in xrange(LOOP):
    pool.spawn(count, NUM)
pool.waitall()
stop = time.time()
elapsed_time['Only_eventlet'] = stop - start


# with multiprocessing
def start_eventlet():
    pool = eventlet.GreenPool(200)
    for i in xrange(green_thread_num):
        pool.spawn(count, NUM)
    pool.waitall()

logger.info('With multiprocessing execution')
start = time.time()
import multiprocessing
processes = []
for i in xrange(process_num):
    p = multiprocessing.Process(target=start_eventlet, args=())
    p.start()
    processes.append(p)

for p in processes:
    p.join()

stop = time.time()
elapsed_time['With_Process'] = stop - start

# Compare performance
for key, value in sorted(elapsed_time.iteritems()):
    logger.info("\t" + key + "\t" + str(value))
