import sys
import time
import socket
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import elasticsearch
from elasticsearch import helpers
import yaml
from socketIO_client import SocketIO
import uuid
import threading
import logging

# create logger
logger = logging.getLogger('LCLogger')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
streamHandler.setFormatter(formatter)

# add ch to logger
logger.addHandler(streamHandler)

#Dictionary that will filter incomming log lines.
AVERAGE_RESTIME_DICT={}

usingFilter=False

class AvgResTimeFileHandler(PatternMatchingEventHandler):
    patterns = ["*.yaml"]

    def on_modified(self, event):
        logger.debug('average_responsetime.yaml has been modified')
        with open(event.src_path, 'r') as f:
            global AVERAGE_RESTIME_DICT
            AVERAGE_RESTIME_DICT.clear
            AVERAGE_RESTIME_DICT = yaml.load(f)
        logger.debug(AVERAGE_RESTIME_DICT)

class LogFileHandler(PatternMatchingEventHandler):
    patterns = ["*.log", "ssl_access.log"]
    count = 0
    docs = []
    offset = 0
    es_client = elasticsearch.Elasticsearch("localhost:9200")
    type = ''
    _id = ''

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        logger.debug(self.count)
        if self.count >= 10:
            elasticsearch.helpers.bulk(self.es_client, self.docs)
            self.count = 0
        else:
            with open(event.src_path, 'r') as f:
                if 'ssl' in f.name:
                    self.type = 'https'
                else:
                    self.type = 'http'
                f.seek(self.offset)
                while True:
                    line = f.readline()
                    if not line:
                        self.offset = f.tell()
                        break
                    else:
                        self.append_docs(line)
                        self.count += 1
                        logger.debug(self.docs)
                        logger.info(self.count)

    def on_modified(self, event):
        logger.debug('logfile has been modified')
        self.process(event)

    def on_created(self, event):
        logger.debug('logfile has been created')
        self.process(event)

    def append_docs(self, line):
        es_source = line.split(' ')
        _id = uuid.uuid4()
        request_uri = es_source[6]
        response_code = es_source[8]
        request_method = es_source[5][1:]
        logger.debug(es_source)
        self.docs.append({
            '_index': 'accesslog',
            '_type': self.type,
            '_id': _id,
            '_source': {
                'request_time': es_source[3][1:],
                'server_name': socket.gethostname(),
                'client_ip': es_source[0],
                'request_method': request_method,
                'request_uri': request_uri,
                'protocol': es_source[7][:-1],
                'response_code': response_code,
                'response_time': es_source[9][:-1]
            }
        })

        # AVERAGE_RESTIME_DICT 값 변수로 받아서 처리
        if usingFilter and (response_code != '200' or
           ((request_uri in AVERAGE_RESTIME_DICT[self.type]
           and request_method in AVERAGE_RESTIME_DICT[self.type].get(request_uri))
           and int(es_source[9][:-1]) + int(AVERAGE_RESTIME_DICT[self.type][request_uri][request_method]['extra_time']) >
            int(AVERAGE_RESTIME_DICT[self.type][request_uri][request_method]['res_time']))):
            self.docs.append({
                '_index': 'event',
                '_type': self.type,
                '_source': {
                    'accesslog_id': _id,
                    'request_uri': request_uri,
                    'request_method': es_source[5][1:],
                    'response_time': es_source[9][:-1],
                    'response_code': response_code,
                    'is_checked': False
                }
            })

class SocketIOThread(threading.Thread):

    def getAvgResTime(self,returnDocs):
        logger.debug('####AVERAGE_RESTIME_DICT has been sent by api server####')
        # logger.debug(returnDocs)
        if returnDocs != 'None' :
            with open('average_responsetime.yaml', 'w') as f:
                yaml.dump(returnDocs, f, default_flow_style=False)
                usingFilter=True

    def run(self):
        with SocketIO('localhost', 8000) as socketIO:
            socketIO.emit('getAvgResTime')
            socketIO.on('response',self.getAvgResTime)
            socketIO.wait()

if __name__ == '__main__':

    t = SocketIOThread()
    t.start()

    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(LogFileHandler(), path=args[0] if args else '.')
    observer.schedule(AvgResTimeFileHandler(), path=args[0] if args else '.')
    observer.start()

    try:
        usingFilter=True
        with open('average_responsetime.yaml', 'r') as f:
            AVERAGE_RESTIME_DICT.clear
            AVERAGE_RESTIME_DICT = yaml.load(f)
    except:
        logger.info('There is no average_responsetime.yaml file!!!')
        usingFilter=False


    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
