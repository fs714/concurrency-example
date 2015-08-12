import time
import eventlet
from eventlet import wsgi


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


def start_web_server():
    app = WsgiApp()
    wsgi.server(eventlet.listen(('', 80)), app)
