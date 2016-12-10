# BlackMamba

## ElasticSearch template
- Create index with the template below
```
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
```
- Request's staticstics template
```
{
  "requeststatistics": {
    "order": 0,
    "template": "requeststatistics*",
    "settings": {
      "index": {
        "number_of_shards": "5",
        "number_of_replicas": "0"
      }
    },
    "mappings": {
      "response_time_average": {
        "properties": {
          "request_uri": {
            "index": "not_analyzed",
            "type": "string"
          },
          "request_method": {
            "type": "string"
          },
          "protocol": {
            "type": "string"
          },
          "average_time": {
            "type": "date"
          },
          "reference_time": {
            "type": "date"
          },
          "period": {
            "type": "long"
          }
        }
      }
    },
    "aliases": {

    }
  }
}
```

