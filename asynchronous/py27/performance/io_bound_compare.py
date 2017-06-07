import logging
import threading
import multiprocessing
import requests
import time
from multiprocessing.pool import ThreadPool

logging.basicConfig()
logger = logging.getLogger('multi_http_request')
logger.setLevel(logging.DEBUG)


# url = 'http://www.baidu.com/'
url = 'http://127.0.0.1:1234/1'

LOOP = 1000
elapsed_time = {}


def get_url(site):
    return requests.get(site)
'''
# Sequential execution
logger.info('Sequential execution')
start = time.time()
for i in xrange(LOOP):
    response = get_url(url)
stop = time.time()
elapsed_time['Sequential'] = stop - start
'''
# Threaded execution
logger.info('Threaded exeution')
start = time.time()
threads = []
for i in xrange(LOOP):
    thread = threading.Thread(target=get_url, args=(url,))
    thread.start()
    threads.append(thread)
for t in threads:
    t.join()
stop = time.time()
elapsed_time['Threaded'] = stop - start

# Thread pool execution
logger.info('Thread pool execution')
start = time.time()
pool = ThreadPool(processes=1000)
for i in xrange(LOOP):
    pool.apply_async(get_url, (url,))
pool.close()
pool.join()
stop = time.time()
elapsed_time['ThreadPool(1000)'] = stop - start

# Processed execution
logger.info('Processed execution')
start = time.time()
processes = []
for i in xrange(LOOP):
    process = multiprocessing.Process(target=get_url, args=(url,))
    process.start()
    processes.append(process)
for p in processes:
    p.join()
stop = time.time()
elapsed_time['Processed'] = stop - start

# Multiprocessing pool execution
logger.info('Multiprocessing pool execution')
start = time.time()
pool = multiprocessing.Pool(processes=100)
for i in xrange(LOOP):
    pool.apply_async(get_url, (url, ))
pool.close()
pool.join()
stop = time.time()
elapsed_time['ProcessPool'] = stop - start

# Multiprocessing pool plus thread pool execution
logger.info('Multiprocessing pool(2) plus thread pool(1000) execution')

def threadpool_executor(processes=None, func=None, iterable=None):
    threadpool = ThreadPool(processes=processes)
    threadpool.map(func, iterable)

start = time.time()
cpus = multiprocessing.cpu_count()
pool = multiprocessing.Pool(processes=cpus)
for i in xrange(cpus):
    pool.apply_async(threadpool_executor, (1000, get_url, [url] * (LOOP / cpus)))
pool.close()
pool.join()
stop = time.time()
elapsed_time['MultiProcessingPool(2)_ThreadPool(1000)'] = stop - start

# Compare performance
for key, value in sorted(elapsed_time.iteritems()):
    logger.info("\t" + key + "\t" + str(value))
