import elasticsearch
from elasticsearch import helpers
import json
import mimetypes
from datetime import *

import falcon

class ESController:

    def __init__(self, host):
        self.es_client = elasticsearch.Elasticsearch(host)


class SearchDocs:

    def __init__(self, es_client, data):
        self.es_client = es_client
        self.data = data

    def on_get(self, req, resp):
        docs = self.es_client.search(index=self.data['index'],
        doc_type=self.data['doc_type'],
        body=self.data['body']
        )
        resp.body = json.dumps(docs, indent = 2)
        resp.status = falcon.HTTP_200

# class GetAvgResTime:
#
#     def __init__(self, es_client, data):
#         self.es_client = es_client
#         self.data = data
#
#     def on_get(self, req, resp):
#         self.data['body']['query']['request_time']['lt'] = req.get_param('')
#         docs = self.es_client.search(index = self.data['index'],
#                                 doc_type = self.data['doc_type'],
#                                 body = self.data['body']
#                                 )
#         resp.body = json.dumps(docs, indent = 2)
#         resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
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

        # print(json.dumps(self.data["body"], indent=2))
        # print(json.dumps(docs, indent=2))

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

        resp.body = "{}"
        resp.status = falcon.HTTP_200


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
