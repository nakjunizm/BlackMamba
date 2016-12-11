import elasticsearch
import json
import mimetypes

import falcon

class ESController:

    def __init__(self, host):
        self.es_client = elasticsearch.Elasticsearch(host)

    def search(self, data):
        docs = self.es_client.search(index = data['index'],
                                doc_type = data['doc_type'])
        return docs

if __name__ == '__main__':
    data = {'index':'accesslog', 'doc_type':'HTTP'}
    # es_client = ESController("localhost:9200")
    es = ESController("localhost:9200")
    print(json.dumps(es.search(data), indent = 2))
    # es_client.search(data)
    # es_client = elasticsearch.Elasticsearch("localhost:9200")
    # docs = es_client.search(index = data['index'],
    #                         doc_type = data['doc_type'])
    # print(json.dumps(docs, indent = 2))
