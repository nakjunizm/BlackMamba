import elasticsearch
import json
import mimetypes

import falcon

class ESController:

    def __init__(self, host):
        self.es_client = elasticsearch.Elasticsearch(host)

    # def search(self, data):
    #     docs = self.es_client.search(index = data['index'],
    #                             doc_type = data['doc_type'])
    #     return docs

class SearchDocs:

    def __init__(self, es_client, data):
        self.es_client = es_client
        self.data = data

    def on_get(self, req, resp):
        docs = self.es_client.search(index = self.data['index'],
                                doc_type = self.data['doc_type'],
                                body = self.data['body']
                                )
        # docs = docs['aggregations']['group_by_request_uri']['buckets']
        resp.body = json.dumps(docs, indent = 2)
        resp.status = falcon.HTTP_200

# class MostCalledApis:
#
#     def __init__(self, es_client):
#         self.es_client = es_client
#
#     def on_get(self, req, resp):
#         docs = self.es_client.transport.perform_request(method = 'POST',
#                                     url = '/accesslog/_search',
#                                     body = {
#                                             'size': 0,
#                                             'aggs': {
#                                              'group_by_request_uri': {
#                                                  'terms': {
#                                                      'field': 'request_uri'
#                                                  }
#                                              }
#                                         }
#                                     })
#         resp.body = json.dumps(docs, indent = 2)
#         resp.status = falcon.HTTP_200
#         print(resp.body)

if __name__ == '__main__':
    data = {'index':'accesslog', 'doc_type':'HTTP'}
    # es_client = ESController("localhost:9200")
    es = ESController("localhost:9200")
    # print(json.dumps(es.search(data), indent = 2))
    # es_client.search(data)
    # es_client = elasticsearch.Elasticsearch("localhost:9200")
    # docs = es_client.search(index = data['index'],
    #                         doc_type = data['doc_type'])
    # print(json.dumps(docs, indent = 2))
