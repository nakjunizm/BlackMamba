from flask import Flask, jsonify, make_response, request
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO,emit

import data
import mock_rest

app = Flask(__name__)
app.config['SECRET_KEY']="bl@ckM@mba"
socketio = SocketIO(app, async_mode='eventlet')
CORS(app)

es_client = data.ESController("localhost:9200").es_client
searchDocs = data.SearchDocs(es_client)
getAvgResTime = data.GetAvgResTime(es_client)

@app.route('/data', methods=['GET'])
def getDocs():
    return searchDocs.on_get({'index':'accesslog', 'doc_type':'http', 'body':''})

@app.route('/top10', methods=['GET'])
def getTop10():
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
    return searchDocs.on_get(_top10Query)

@app.route('/avg-res-time', methods=['POST'])
def postResTime():
    req = request
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
    return searchDocs.on_post(req, _avgResTimeQuery)

@app.route('/avg-res-time/updateCollector', methods=['GET'])
def updateCollector():
    returnDocs = getAvgResTimeDocs()
    socketio.emit('response', returnDocs)
    return make_response(jsonify('{"message":"ok"}'),200)

@app.route('/event')
def event_test():
    return mock_rest.MockEventAPI()

@app.route('/event{id}')
def event_test_withId():
    return mock_rest.MockEventAPI()

@socketio.on('connect')
def connect():
    print('Client connected')

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

@socketio.on('getAvgResTime')
def getAvgResTimeOn():
    try:
        returnDocs = getAvgResTimeDocs()
    except:
        returnDocs = 'None'
    emit('response', returnDocs)

def getAvgResTimeDocs():
    _latestAvgResTimeQuery1 = {
        'index': 'response_average',
        'body': {
                'size' : 1,
                'sort' : [
                    { 'created_time' :
                    { 'order' : 'desc' }}
                ]
            }
        }

    _latestAvgResTimeQuery2 = {
        'index': 'response_average',
        'body': {
                'size' : 100,
                'query' : {
                    'term': {
                        'created_time': ''
                    }
                }
            }
        }
    return getAvgResTime.on_get([_latestAvgResTimeQuery1,_latestAvgResTimeQuery2],'http')

if __name__ == '__main__':
    #app.run(host='localhost', port=8000, debug=True)
    socketio.run(app, host='localhost', port=8000, debug=True)
