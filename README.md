# BlackMamba

## ElasticSearch template
- Create index with the template below
'''
{
  "accesslog": {
    "order": 0,
    "template": "accsess*",
    "settings": {
      "index": {
        "number_of_shards": "5",
        "number_of_replicas": "0"
      }
    },
    "mappings": {
      "HTTP": {
        "properties": {
          "server_name": {
            "type": "string"
          },
          "protocol": {
            "type": "string"
          },
          "response_code": {
            "type": "string"
          },
          "request_time": {
            "type": "string"
          },
          "client_ip": {
            "type": "string"
          },
          "response_time": {
            "type": "string"
          },
          "request_method": {
            "type": "string"
          },
          "request_uri": {
            "index": "not_analyzed",
            "type": "string"
          }
        }
      },
      "HTTPS": {
        "properties": {
          "server_name": {
            "type": "string"
          },
          "protocol": {
            "type": "string"
          },
          "response_code": {
            "type": "string"
          },
          "request_time": {
            "type": "string"
          },
          "client_ip": {
            "type": "string"
          },
          "response_time": {
            "type": "string"
          },
          "request_method": {
            "type": "string"
          },
          "request_uri": {
            "index": "not_analyzed",
            "type": "string"
          }
        }
      }
    },
    "aliases": {

    }
  }
}
'''


