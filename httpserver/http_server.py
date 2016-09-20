import time
import logging
import eventlet
from eventlet import wsgi

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Monkey patch socket, time, select, threads
eventlet.patcher.monkey_patch(all=False, socket=True, time=True,
                              select=True, thread=True, os=True)


class WsgiApp(object):
    def __init__(self):
        print('WsgiApp init')

    def __call__(self, environ, start_response):
        sleep_time = float(environ.get('PATH_INFO').split('/')[1])
        time.sleep(sleep_time)
        body = ["Hello World"]
        start_response('200 OK', [('Content-Type', 'application/json')])
        return body


class Server(object):
    def __init__(self, threads=1000, workers=4, logger=logger):
        self.threads = threads
        self.workers = workers
        self.logger = logger


def start_web_server():
    app = WsgiApp()
    workers = 4

    '''
    wsgi.server(eventlet.listen(('', 80)), app)
    '''

    '''
    import os
    socket = eventlet.listen(('', 80))
    for i in xrange(workers):
        pid = os.fork()
        if pid == 0:
            # wsgi.server(eventlet.listen(('', 80)), app)
            wsgi.server(socket, app)
        else:
            print('Started child %s' % pid)
    '''

    import multiprocessing
    socket = eventlet.listen(('', 1234))

    def start(socket, app):
        wsgi.server(socket, app)

    for i in xrange(workers):
        p = multiprocessing.Process(target=start, args=(socket, app))
        p.start()
