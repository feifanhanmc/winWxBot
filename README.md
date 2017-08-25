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

4.3 数据类型表
| `type` | 数据类型 | `data` |
| ---- | ---- | ------ |
| 0 | 文本 | 字典，包含data(表示文本消息的具体内容) |
| 1 | 地理位置 | 字典，包含data(表示地理位置)|
| 3 | 图片 | 字典，包含data(图片数据的url，HTTP POST请求此url可以得到jpg文件格式的数据) |
| 4 | 语音 | 字典，包含data(语音数据的url，HTTP POST请求此url可以得到mp3文件格式的数据) |
| 5 | 名片 | 字典，包含 `nickname` (昵称)， `alias` (别名)，`province` (省份)，`city` (城市)， `gender` (性别)字段 |
| 6 | 动画 | 字典，包含data(动画url, HTTP POST请求此url可以得到gif文件格式的数据) |
| 7 | 分享 | 字典，包含 `type` (类型)，`title` (标题)，`desc` (描述)，`url` (链接)，`from` (源网站)字段 |
| 8 | 视频 | 不可用 |
| 9 | 视频电话 | 不可用 |
| 10 | 撤回消息 | 不可用 |
| 11 | 空内容 | 字典，包含data(空字符串) |
| 12 | 红包 | 不可用 |
| 13 | 小视频 | 字典，包含data(视频数据的url，HTTP POST请求此url可以得到mp4文件格式的数据) |
| 99 | 未知类型 | 不可用 |