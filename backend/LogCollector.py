import sys
import time
import socket
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import elasticsearch
from elasticsearch import helpers
import yaml
import uuid

AVERAGE_RESTIME_DICT={}

class AvgResTimeFileHandler(PatternMatchingEventHandler):
    patterns = ["average_responsetime.yaml"]

    def on_modified(self, event):

        with open(event.src_path, 'r') as f:
            global AVERAGE_RESTIME_DICT
            AVERAGE_RESTIME_DICT.clear
            AVERAGE_RESTIME_DICT = yaml.load(f)
        print(AVERAGE_RESTIME_DICT)

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

        if self.count >= 10:
            elasticsearch.helpers.bulk(self.es_client, self.docs)
            #print(self.docs)
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
                        print(self.docs)
                        print(self.count)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

    def append_docs(self, line):
        es_source = line.split(' ')
        _id = uuid.uuid4()
        request_uri = es_source[6]
        response_code = es_source[8]
        print(es_source)
        self.docs.append({
            '_index': 'accesslog',
            '_type': self.type,
            '_id': _id,
            '_source': {
                'request_time': es_source[3][1:],
                'server_name': socket.gethostname(),
                'client_ip': es_source[0],
                'request_method': es_source[5][1:],
                'request_uri': request_uri,
                'protocol': es_source[7][:-1],
                'response_code': response_code,
                'response_time': es_source[9][:-1]
            }
        })

        if response_code != '200' or (request_uri in AVERAGE_RESTIME_DICT[self.type] and int(es_source[9][:-1]) + int(AVERAGE_RESTIME_DICT[self.type]['extra_time']) > int(AVERAGE_RESTIME_DICT[self.type][es_source[6]])):
            self.docs.append({
                '_index': 'event',
                '_type': self.type,
                '_source': {
                    'accesslog_id': _id,
                    'request_uri': request_uri,
                    'request_method': es_source[5][1:],
                    'response_time': es_source[9][:-1],
                    'response_code': response_code,
                    'is_checked': 'False'
                }
            })

if __name__ == '__main__':

    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(LogFileHandler(), path=args[0] if args else '.')
    observer.start()

    with open('average_responsetime.yaml', 'r') as f:
        AVERAGE_RESTIME_DICT.clear
        AVERAGE_RESTIME_DICT = yaml.load(f)

    print(AVERAGE_RESTIME_DICT)

    avgObserver = Observer()
    avgObserver.schedule(AvgResTimeFileHandler, path='.')
    avgObserver.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
