# winWxBot
{
  "mappings": {
    "msg_text": {
      "properties": {
        "to_user_id": {
          "type": "string"
        },
        "msg_id": {
          "type": "string"
        },
        "msg_type_id": {
          "type": "long"
        },
        "user": {
          "properties": {
            "name": {
              "type": "string"
            },
            "id": {
              "type": "string"
            }
          }
        },
        "content": {
          "properties": {
            "data": {
              "properties": {
                "data": {
                  "type": "string"
                },
                "gender": {
                  "type": "string"
                },
                "province": {
                  "type": "string"
                },
                "city": {
                  "type": "string"
                },
                "nickname": {
                  "type": "string"
                },
                "alias": {
                  "type": "string"
                },
                "from": {
                  "type": "string"
                },
                "title": {
                  "type": "string"
                },
                "type": {
                  "type": "string"
                },
                "content": {
                  "type": "string"
                },
                "url": {
                  "type": "string"
                },
                "desc": {
                  "type": "string"
                }
              }
            },
            "detail": {
              "properties": {
                "type": {
                  "type": "string"
                },
                "value": {
                  "type": "string"
                }
              }
            },
            "type": {
              "type": "long"
            },
            "user": {
              "properties": {
                "name": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                }
              }
            },
            "desc": {
              "type": "string"
            }
          }
        }
      }
    }
  }
}