import falcon
import data
from wsgiref import simple_server

api = application = falcon.API()

es_client = data.ESController("localhost:9200").es_client
print (type(es_client))
docs = data.SearchDocs(es_client)

# api.add_route('/images', image_collection)
# api.add_route('/images/{name}', image)
api.add_route('/data',docs)

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, api)
    httpd.serve_forever()
