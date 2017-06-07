import eventlet
from eventlet.green import urllib2
import logging
import time
import requests


logging.basicConfig()
logger = logging.getLogger('eventlet')
logger.setLevel(logging.DEBUG)

LOOP = 1000
URL = 'http://127.0.0.1:1234/1'
elapsed_time = {}


def fetch(url):
    body = urllib2.urlopen(url).read()
    return url, body


def get_url(url):
    return requests.get(url)


# With green urllib
logger.info('With green urllib')
start = time.time()
pool = eventlet.GreenPool(1000)
for i in xrange(LOOP):
    pool.spawn(fetch, URL)
pool.waitall()
stop = time.time()
elapsed_time['Green_Urllib'] = stop - start


# With monkey patched requests
eventlet.patcher.monkey_patch(all=True)

logger.info('With monkey patched requests')
start = time.time()
pool = eventlet.GreenPool(1000)
for i in xrange(LOOP):
    pool.spawn(get_url, URL)
pool.waitall()
stop = time.time()
elapsed_time['Patched_Requests'] = stop - start

# Compare performance
for key, value in sorted(elapsed_time.iteritems()):
    logger.info("\t" + key + "\t" + str(value))
