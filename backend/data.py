import elasticsearch
from elasticsearch import helpers
from flask import jsonify, make_response
import json
import mimetypes
from datetime import datetime, date
from collections import defaultdict
import math

import yaml

class ESController:

    def __init__(self, host):
        self.es_client = elasticsearch.Elasticsearch(host)


class SearchDocs:

    def __init__(self, es_client):
        self.es_client = es_client

    def on_get(self, data):
        self.data = data
        docs = self.es_client.search(index = self.data['index'],
                                doc_type = self.data['doc_type'],
                                body = self.data['body']
                                )
        return make_response(jsonify(docs),'200')

    def on_post(self, req, data):
        self.data = data
        query = { "range" : {
            "request_time" : {
                "gte": date.today().isoformat(),
                "lte": "",
                "format": "date"
             }
            }
        }
        body = json.loads(req.stream.read().decode('utf-8'))

        ref_str = body["reference_date_from"].split("-")
        reference_date_from = date(int(ref_str[0]), int(ref_str[1]), int(ref_str[2]))
        query["range"]["request_time"]["gte"] = reference_date_from.isoformat()

        ref_str = body["reference_date_to"].split("-")
        reference_date_to = date(int(ref_str[0]), int(ref_str[1]), int(ref_str[2]))
        query["range"]["request_time"]["lte"] = reference_date_to.isoformat()

        self.data["body"]["query"] = query

        docs = self.es_client.search(index=self.data["index"],
            doc_type=self.data["doc_type"], body=self.data["body"]
        )

        print(json.dumps(self.data["body"], indent=2))
        print(json.dumps(docs, indent=2))

        input_data = []
        created_time = str(datetime.today().timestamp()).split(".")[0]
        for uri in docs["aggregations"]["group_by_request_uri"]["buckets"]:
            print(uri["key"])
            for method in uri["by_request_method"]["buckets"]:
                input_data.append({
                    "_index": "response_average",
                    "_type": self.data["doc_type"],
                    "_source": {
                        "request_uri": uri["key"],
                        "request_method": method["key"],
                        "average_time": method["response_time_avg"]["value"],
                        "reference_time_from": reference_date_from.isoformat(),
                        "reference_time_to": reference_date_to.isoformat(),
                        "created_time": created_time
                    }
                })

        elasticsearch.helpers.bulk(self.es_client, input_data)
        return make_response(jsonify('{"message":"ok"}'),200)

class GetAvgResTime:

    def __init__(self, es_client):
        self.es_client = es_client

    def on_get(self, query, doc_type):
        self.query1 = query[0]
        self.query2 = query[1]
        self.doc_type = doc_type
        created_time = self.es_client.search(index = self.query1['index'],
                                    doc_type = self.doc_type,
                                    body = self.query1['body']
                                )
        self.query2['body']['query']['term']['created_time'] = str(created_time['hits']['hits'][0]['sort'][0])

        docs = self.es_client.search(index = self.query2['index'],
                                doc_type = self.doc_type,
                                body = self.query2['body'])

        DEFAULT_EXTRA = 1000
        avg_response_yaml = {}
        for doc in docs['hits']['hits']:
            data = {doc['_type']:{doc['_source']['request_uri']:{doc['_source']['request_method']:
            {'res_time' : int(math.ceil(doc['_source']['average_time'])),
             'extra_time' : DEFAULT_EXTRA}
            }}}
            print(data)
            key = frozenset(data.items())
            if key[doc['_type']] in avg_response_yaml:
                if data[doc['_type']][doc['_source']['request_uri']] in avg_response_yaml:
                    if data[doc['_type']][doc['_source']['request_uri']][doc['_source']['request_method']] in avg_response_yaml:
                        avg_response_yaml.update(data[doc['_type']][doc['_source']['request_uri']][doc['_source']['request_method']])
                    else : avg_response_yaml.update(data[doc['_type']][doc['_source']['request_uri']])
                else : avg_response_yaml.update(data[doc['_type']])
            # avg_response_yaml[self.doc_type][doc['_source']['request_uri']][doc['_source']['request_method']]['res_time'] = int(math.ceil(doc['_source']['average_time']))
            # avg_response_yaml[self.doc_type][doc['_source']['request_uri']][doc['_source']['request_method']]['extra_time'] = DEFAULT_EXTRA

        print (avg_response_yaml)
        # with open('data.yml', 'w') as outfile:
        #     yaml.dump(avg_response_yaml, outfile, default_flow_style=True)

        return avg_response_yaml

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
