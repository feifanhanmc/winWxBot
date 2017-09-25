# winWxBot


```
{
  "wx_xnr": {
    "mappings": {
      "groupmsg": {
        "properties": {
          "data": {
            "properties": {
              "recommend": {
                "properties": {
                  "alias": {
                    "type": "string",
                    "index": "not_analyzed"
                  },
                  "city": {
                    "type": "string",
                    "index": "not_analyzed"
                  },
                  "gender": {
                    "type": "string",
                    "index": "not_analyzed"
                  },
                  "nickname": {
                    "type": "string",
                    "index": "not_analyzed"
                  },
                  "province": {
                    "type": "string",
                    "index": "not_analyzed"
                  }
                }
              },
              "share": {
                "properties": {
                  "from": {
                    "type": "string",
                    "index": "not_analyzed"
                  },
                  "title": {
                    "type": "string",
                    "index": "not_analyzed"
                  },
                  "url": {
                    "type": "string",
                    "index": "not_analyzed"
                  }
                }
              },
              "str": {
                "type": "string",
                "index": "not_analyzed"
              }
            }
          },
          "timestamp": {
            "type": "long"
          },
          "group_id": {
            "type": "string",
            "index": "not_analyzed"
          },
          "group_name": {
            "type": "string",
            "index": "not_analyzed"
          },
          "msg_type": {
            "type": "string",
            "index": "not_analyzed"
          },
          "speaker_id": {
            "type": "string",
            "index": "not_analyzed"
          },
          "speaker_name": {
            "type": "string",
            "index": "not_analyzed"
          }
        }
      }
    }
  }
}
```


