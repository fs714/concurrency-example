import eventlet
import logging
import time

eventlet.patcher.monkey_patch(all=True)

logging.basicConfig()
logger = logging.getLogger('eventlet')
logger.setLevel(logging.DEBUG)

LOOP = 5
NUM = 100000000
elapsed_time = {}


def count(n):
    while n > 0:
        n = n - 1

# With green urllib
logger.info('Eventlet execution')
start = time.time()
pool = eventlet.GreenPool(200)
for i in xrange(LOOP):
    pool.spawn(count, NUM)
pool.waitall()
stop = time.time()
elapsed_time['Green_Urllib'] = stop - start


# Compare performance
for key, value in sorted(elapsed_time.iteritems()):
    logger.info("\t" + key + "\t" + str(value))
