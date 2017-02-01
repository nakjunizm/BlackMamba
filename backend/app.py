import falcon
from falcon_cors import CORS
import data
from wsgiref import simple_server
import mock_rest

cors = CORS(allow_all_origins=True,
            allow_all_methods=True,
            allow_all_headers=True)
api = application = falcon.API(middleware=[cors.middleware])

es_client = data.ESController("localhost:9200").es_client
docs = data.SearchDocs(es_client, {'index':'accesslog', 'doc_type':'http', 'body':''})
# _top10Query = {'index':'accesslog','doc_type':'http',
#           'body': {
#                     'size': 0,
#                     'aggs': {
#                                 'group_by_request_uri': {
#                                         'terms': {
#                                             'field': 'request_uri'
#                                         }
#                                  }
#                             }
#                     }
#             }
_top10Query = {'index':'accesslog',
    'doc_type':'http',
    'body': {
        'size': 0,
        'aggs': {
            'avg_response_time': {
                'terms': { 'field': 'request_uri' }
            }
        }
    }
}
top10 = data.SearchDocs(es_client, _top10Query)

_avgResTimeQuery = {
    "index": "accesslog",
    "doc_type":"http",
    "body": {
        "size": 0,
        "aggs": {
            "group_by_request_uri": {
                "terms": {
                    "field": "request_uri"
                },
                "aggs": {
                    "by_request_method" : {
                        "terms": {
                            "field": "request_method"
                        },
                        "aggs": {
                            "response_time_avg": { "avg": { "field": "response_time" } }
                        }
                    }
                }
            }
        }
    }
}
avgResTime = data.SearchDocs(es_client, _avgResTimeQuery)


api.add_route('/data',docs)
api.add_route('/top10',top10)
api.add_route('/avg-res-time',avgResTime)

# For test
api.add_route('/event', mock_rest.MockEventAPI())
api.add_route('/event/{id}', mock_rest.MockEventAPI())

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, api)
    httpd.serve_forever()
