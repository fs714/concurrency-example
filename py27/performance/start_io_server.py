import os
import sys
sys.path.append(os.path.abspath(
    os.path.abspath(os.path.dirname(__file__)) + '/../'))
from httpserver.http_server import start_web_server
import multiprocessing


web_server = multiprocessing.Process(target=start_web_server, args=())
web_server.start()
