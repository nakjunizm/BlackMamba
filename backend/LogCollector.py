import sys
import time, os.path
import datetime
import socket
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import elasticsearch
from elasticsearch import helpers
import yaml
from socketIO_client import SocketIO
import uuid
import threading
import logging.config, os, yaml
import LCParam

loggingConfigPath = './conf/logging.yaml'
if os.path.exists(loggingConfigPath):
    with open(loggingConfigPath, 'rt') as logconf:
        loggingConfig = yaml.load(logconf.read())
        logging.config.dictConfig(loggingConfig)
else:
    logging.basicConfig(level=logging.INFO)

class AvgResTimeFileHandler(PatternMatchingEventHandler):

    patterns = ["*.yaml"]
    def __init__(self):
        super().__init__(self)
        self.average_restime_dict = LCParam.AVERAGE_RESTIME_DICT

    def on_modified(self, event):
        logging.debug('average_responsetime.yaml has been modified')
        with open(event.src_path, 'r') as ast:
            self.average_restime_dict = yaml.load(ast)
        logging.debug(self.average_restime_dict)

class AccessLogFileHandler(PatternMatchingEventHandler):

    patterns = ["*access.log"]
    es_client = elasticsearch.Elasticsearch("localhost:9200")
    def __init__(self):
        super().__init__(self)
        self.count = 0
        self.docs = []
        self.offsetDict = dict()
        self.offset = LCParam.ACCESSLOG_OFFSET
        logging.info('*****offset******: %d', self.offset)
        logging.info(LCParam.AVERAGE_RESTIME_DICT)
        self.type = 'http'
        self._id = ''
        self.average_restime_dict = LCParam.AVERAGE_RESTIME_DICT
        logging.info('in __init__ access %s',self.average_restime_dict)

    def process(self, event):
        logging.info('*****offset!******: %d', self.offset)
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        logging.debug(self.count)
        if self.count >= 10:
            elasticsearch.helpers.bulk(self.es_client, self.docs)
            with open('./conf/offset', 'w') as offsetConf:
                self.offsetDict['http'] = self.offset
                yaml.dump(self.offsetDict, offsetConf, default_flow_style=False)
            self.count = 0
        else:
            with open(event.src_path, 'r') as f:
                f.seek(self.offset)
                while True:
                    line = f.readline()
                    if not line:
                        self.offset = f.tell()
                        break
                    else:
                        self.append_docs(line)
                        self.count += 1
                        logging.debug(self.docs)
        logging.info(self.count)

    def on_modified(self, event):
        logging.debug('logfile has been modified')
        self.process(event)

    def on_created(self, event):
        logging.debug('logfile has been created')
        self.process(event)

    def append_docs(self, line):
        logging.info('in append_docs %s', self.average_restime_dict)
        es_source = line.split(' ')
        self._id = uuid.uuid4()
        request_uri = es_source[6]
        response_code = es_source[8]
        request_method = es_source[5][1:]
        logging.debug(es_source)
        self.docs.append({
            '_index': 'accesslog',
            '_type': self.type,
            '_id': self._id,
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
        if LCParam.FILTER and (response_code != '200' or
           ((request_uri in self.average_restime_dict[self.type]
           and request_method in self.average_restime_dict[self.type].get(request_uri))
           and int(es_source[9][:-1]) + int(self.average_restime_dict[self.type][request_uri][request_method]['extra_time']) >
            int(self.average_restime_dict[self.type][request_uri][request_method]['res_time']))):
            self.docs.append({
                '_index': 'event',
                '_type': self.type,
                '_source': {
                    'accesslog_id': self._id,
                    'request_uri': request_uri,
                    'request_method': es_source[5][1:],
                    'response_time': es_source[9][:-1],
                    'response_code': response_code,
                    'is_checked': 'false'
                }
            })

class SslAccessLogFileHandler(PatternMatchingEventHandler):

    patterns = ["*ssl_access.log"]
    es_client = elasticsearch.Elasticsearch("localhost:9200")
    def __init__(self):
        super().__init__(self)
        self.count = 0
        self.docs = []
        self.offsetDict = {}
        self.offset = LCParam.SSL_ACCESSLOG_OFFSET
        self.type = 'https'
        self._id = ''
        self.average_restime_dict = LCParam.AVERAGE_RESTIME_DICT
        logging.info('in __init__ sslaccess %s',LCParam.AVERAGE_RESTIME_DICT)

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        logging.debug(self.count)
        if self.count >= 10:
            elasticsearch.helpers.bulk(self.es_client, self.docs)
            with open('./conf/offset', 'w') as offsetConf:
                self.offsetDict['http'] = self.offset
                yaml.dump(self.offsetDict, offsetConf, default_flow_style=False)
            self.count = 0
        else:
            with open(event.src_path, 'r') as f:
                f.seek(self.offset)
                while True:
                    line = f.readline()
                    if not line:
                        self.offset = f.tell()
                        break
                    else:
                        self.append_docs(line)
                        self.count += 1
                        logging.debug(self.docs)
                        logging.info(self.count)

    def on_modified(self, event):
        logging.debug('logfile has been modified')
        self.process(event)

    def on_created(self, event):
        logging.debug('logfile has been created')
        self.process(event)

    def append_docs(self, line):
        es_source = line.split(' ')
        self._id = uuid.uuid4()
        request_uri = es_source[6]
        response_code = es_source[8]
        request_method = es_source[5][1:]
        logging.debug(es_source)
        self.docs.append({
            '_index': 'accesslog',
            '_type': self.type,
            '_id': self._id,
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
        if LCParam.FILTER and (response_code != '200' or
           ((request_uri in self.average_restime_dict[self.type]
           and request_method in self.average_restime_dict[self.type].get(request_uri))
           and int(es_source[9][:-1]) + int(self.average_restime_dict[self.type][request_uri][request_method]['extra_time']) >
            int(self.average_restime_dict[self.type][request_uri][request_method]['res_time']))):
            self.docs.append({
                '_index': 'event',
                '_type': self.type,
                '_source': {
                    'accesslog_id': self._id,
                    'request_uri': request_uri,
                    'request_method': es_source[5][1:],
                    'response_time': es_source[9][:-1],
                    'response_code': response_code,
                    'is_checked': 'false'
                }
            })

class SocketIOThread(threading.Thread):

    def getAvgResTime(self,returnDocs):
        logging.debug('####AVERAGE_RESTIME_DICT has been sent by api server####')
        #logging.debug(returnDocs)
        if returnDocs != 'None' :
            with open('average_responsetime.yaml', 'w') as art:
                yaml.dump(returnDocs, art, default_flow_style=False)
                LCParam.FILTER=True

    def run(self):
        with SocketIO('localhost', 8000) as socketIO:
            socketIO.emit('getAvgResTime')
            socketIO.on('response', self.getAvgResTime)
            socketIO.wait()

if __name__ == '__main__':
    
    try:
        with open('average_responsetime.yaml', 'r') as art:
            LCParam.AVERAGE_RESTIME_DICT = yaml.load(art)
            LCParam.FILTER = True
            #logging.info(LCParam.AVERAGE_RESTIME_DICT)
    except:
        logging.error('There is no average_responsetime.yaml file!!!')
        LCParam.FILTER = False

    #1. Check if there is a offset file
    try:
        with open('./conf/offset', 'r') as of:
            # If the created time of an offset file is behind today, consider that the apache log files were rolled and offset is useless.
            t = os.path.getmtime('./conf/offset')
            offsetCreatedDate = datetime.date.fromtimestamp(t)
            if offsetCreatedDate.month == datetime.datetime.now().month and offsetCreatedDate.day == datetime.datetime.now().day:
                offsets = yaml.load(of)
                if 'http' in offsets.keys():
                    LCParam.ACCESSLOG_OFFSET = offsets['http']
                if 'https' in offsets.keys():
                    LCParam.SSL_ACCESSLOG_OFFSET = offsets['https']
            else :
                LCParam.ACCESSLOG_OFFSET = 0
                LCParam.SSL_ACCESSLOG_OFFSET = 0
            logging.info('ACCESSLOG_OFFSET: %d', LCParam.ACCESSLOG_OFFSET)
            logging.info('SSL_ACCESSLOG_OFFSET: %d', LCParam.SSL_ACCESSLOG_OFFSET)
    except:
        logging.error('Exception occured during opening the offset file.')
    
    #2. SocketIO
    t = SocketIOThread()
    t.start()

    #3. Observe files
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(AccessLogFileHandler(), path=args[0] if args else '.')
    observer.schedule(SslAccessLogFileHandler(), path=args[0] if args else '.')
    observer.schedule(AvgResTimeFileHandler(), path=args[0] if args else '.')
    observer.start()



    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
