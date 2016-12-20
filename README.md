# BlackMamba

## ElasticSearch template
### Create index with the template below
```
{
  "order": 0,
  "template": "access*",
  "settings": {
    "index": {
      "number_of_shards": "5",
      "number_of_replicas": "0"
    }
  },
  "mappings": {
    "http": {
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
          "format": "dd/MMM/yyyy:HH:mm:ss",
          "type": "date"
        },
        "client_ip": {
          "type": "string"
        },
        "response_time": {
          "type": "long"
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
    "https": {
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
          "format": "dd/MMM/yyyy:HH:mm:ss",
          "type": "date"
        },
        "client_ip": {
          "type": "string"
        },
        "response_time": {
          "type": "long"
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
  "aliases": {}
}
```
### Request's response_average template
```
{
  "order": 0,
  "template": "response_average*",
  "settings": {
    "index": {
      "number_of_shards": "5",
      "number_of_replicas": "0"
    }
  },
  "mappings": {
    "http": {
      "properties": {
        "request_uri": {
          "index": "not_analyzed",
          "type": "string"
        },
        "request_method": {
          "type": "string"
        },
        "average_time": {
          "type": "long"
        },
        "reference_time_from": {
          "type": "date"
        },
        "reference_time_to": {
          "type": "date"
        },
        "created_time": {
          "type": "date"
        }
      }
    },
    "https": {
      "properties": {
        "request_uri": {
          "index": "not_analyzed",
          "type": "string"
        },
        "request_method": {
          "type": "string"
        },
        "average_time": {
          "type": "long"
        },
        "reference_time_from": {
          "type": "date"
        },
        "reference_time_to": {
          "type": "date"
        },
        "created_time": {
          "type": "date"
        }
      }
    }
  },
  "aliases": {

  }
}
```
### Event template
```
{
  "order": 0,
  "template": "event*",
  "settings": {
    "index": {
      "number_of_shards": "5",
      "number_of_replicas": "0"
    }
  },
  "mappings": {
    "http": {
      "properties": {
        "accesslog_id": {
          "type": "string"
        },
        "request_uri": {
          "index": "not_analyzed",
          "type": "string"
        },
        "request_method": {
          "type": "string"
        },
        "response_time": {
          "type": "long"
        },
        "response_code": {
          "type": "string"
        },
        "is_checked": {
          "type": "boolean"
        }
      }
    },
    "https": {
      "properties": {
        "accesslog_id": {
          "type": "string"
        },
        "request_uri": {
          "index": "not_analyzed",
          "type": "string"
        },
        "request_method": {
          "type": "string"
        },
        "response_time": {
          "type": "long"
        },
        "response_code": {
          "type": "string"
        },
        "is_checked": {
          "type": "boolean"
        }
      }
    }
  },
  "aliases": {

  }
}
```
