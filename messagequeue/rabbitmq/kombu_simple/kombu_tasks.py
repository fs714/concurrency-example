import os
import time
import logging

logging.basicConfig()
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.DEBUG)


def get_url_task(url, delay):
    time.sleep(delay)
    logger.info('Request URL: ' + url + '/' + str(delay) + '/')


def echo_task(info, delay):
    time.sleep(delay)
    logger.info('Echo Information: ' + info)
