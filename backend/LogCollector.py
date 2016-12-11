import sys
import time
import socket
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import elasticsearch
from elasticsearch import helpers


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.log", "ssl_access.log"]
    count = 0
    docs = []
    offset = 0
    es_client = elasticsearch.Elasticsearch("localhost:9200")
    type = ''

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
                    self.type = 'HTTPS'
                else:
                    self.type = 'HTTP'
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
        print(es_source)
        self.docs.append({
            '_index': 'accesslog',
            '_type': self.type,
            '_source': {
                'request_time': es_source[3][1:],
                'server_name': socket.gethostname(),
                'client_ip': es_source[0],
                'request_method': es_source[5][1:],
                'request_uri': es_source[6],
                'protocol': es_source[7][:-1],
                'response_code': es_source[8],
                'response_time': es_source[9][:-1]
            }
        })

if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(MyHandler(), path=args[0] if args else '.')
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
