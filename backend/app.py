import falcon
from falcon_cors import CORS
import data
from wsgiref import simple_server

cors = CORS(allow_all_origins=True)
api = application = falcon.API(middleware=[cors.middleware])

es_client = data.ESController("localhost:9200").es_client
docs = data.SearchDocs(es_client, {'index':'accesslog', 'doc_type':'HTTP', 'body':''})
_top10Query = {'index':'accesslog',
          'doc_type':'HTTP',
          'body': {
                    'size': 0,
                    'aggs': {
                                'group_by_request_uri': {
                                        'terms': {
                                            'field': 'request_uri'
                                        }
                                 }
                            }
                    }
            }

top10 = data.SearchDocs(es_client, _top10Query)

_top10Query = {'index':'accesslog',
          'doc_type':'HTTP',
          'body': {
                    'size': 0,
                    'aggs': {
                                'avg_response_time': {
                                        'field': 'request_uri'
                                 }
                            }
                    }
            }

_avgResTimeQuery = {''}          
avgResTime = data.SearchDocs(es_client, _avgResTimeQuery)


api.add_route('/data',docs)
api.add_route('/top10',top10)

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, api)
    httpd.serve_forever()
