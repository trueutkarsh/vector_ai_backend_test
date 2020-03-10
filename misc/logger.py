"""
This is the logging module which will initialize a logger 
 and provide a get_logger function to the rest of the system.
 It will be a wrapper around logstash
"""

import logging
import logstash

global logger

host = 'localhost'

logger = logging.getLogger('python-logstash-logger')
logger.addHandler(logstash.LogstashHandler(host, 5959, version=1))


def get_logger(level=logging.INFO):
    logger.setLevel(logging.INFO)
    return logger
    

