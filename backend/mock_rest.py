# -*- coding: utf-8 -*-
import json

import elasticsearch
from elasticsearch import helpers
import falcon


class MockEventAPI:

    def __init__(self, host='localhost:9200'):
        self.es_client = elasticsearch.Elasticsearch(host)


    def on_get(self, req, resp):
        # Only search data in which is_checked's value is False
        query = dict()
        query['term'] = dict()
        query['term']['is_checked'] = False
        body = dict()
        body['query'] = query
        index = 'event'

        es_docs = self.es_client.search(index=index, body=body)

        rst = list()
        for hit in es_docs['hits']['hits']:
            rst.append(self._convert_js(hit['_id'], hit['_type'], hit['_source']))

        resp.body = json.dumps({"rst": rst})
        # resp.body = json.dumps(es_docs)
        resp.status = falcon.HTTP_200


    def on_put(self, req, resp, id):
        body = json.loads(req.stream.read().decode('utf-8'))
        # print("id: " + id)
        # print("doc_type: " + body['doc_type'])
        # print(req.headers)
        doc = dict()
        doc['is_checked'] = True

        es_doc = self.es_client.update(index='event', id=id, doc_type=body['doc_type'],
                                body={'doc': doc})
        resp.body = json.dumps(es_doc)
        resp.status = falcon.HTTP_200


    def _convert_js(self, _id, _type, source):
        rst = dict()
        rst['id'] = _id
        rst['type'] = _type
        rst['isChecked'] = False
        rst['accesslogId'] = source['accesslog_id']
        rst['requestUri'] = source['request_uri']
        rst['requestMethod'] = source['request_method']
        rst['responseTime'] = source['response_time']
        rst['responseCode'] = source['response_code']

        return rst
