# -*- coding: utf-8 -*-
import json
from elasticsearch import Elasticsearch

class WX_XNR_ES():
    def __init__(self, host='hanmengcheng.com:9200', index_name='wx_xnr'):
        self.es = Elasticsearch(host)
        self.index_name = index_name
    
    def create_index(self, mappings={}, index_name=None, params=None):
        #create a index without replicas
        if index_name:
            self.index_name = index_name
        if not self.es.indices.exists(index=self.index_name):
            return self.es.indices.create(index=self.index_name, ignore=400, body={
                'settings':{
                    'number_of_shards':5,
                    'number_of_replicas':0,
                },
                'mappings':mappings
            })
        
    def put_mapping(self, doc_type, mapping={}, index_name=None):
        #实际上是通过put_mapping的方式规定一个doc_type的mapping，但其实有些不符合该mapping的数据也能存储进来，并改变mapping
        if index_name:
            self.index_name = index_name
        return self.es.indices.put_mapping(doc_type, body=mapping, index=self.index_name)
    
    def save_data(self, doc_type, data, data_id=None, index_name=None):
        #data(dict)
        if index_name:
            self.index_name = index_name
        return self.es.index(index=self.index_name, doc_type=doc_type, body=json.JSONEncoder().encode(data), id=data_id)
        
    
if __name__ == '__main__':
    es = WX_XNR_ES()
#     print es.create_index()
#     test_mapping = {
#         'properties':{
#             'm':{
#                 'type': 'string'
#             },
#             'msg_id':{
#                 'type': 'long'
#             }
#         }
#     }
#     print es.put_mapping('test2', mapping=test_mapping)
    data = {
        "content": {
            "data": {
              "text": "\u6211\u64e6\uff0c\u741b\u54e5\u771f\u53f8\u673a"
            },
            "desc": "\u6211\u64e6\uff0c\u741b\u54e5\u771f\u53f8\u673a",
            "type": 0,
            "user": {
              "id": "@644982a9264ad1ebeeab1d010de94ddf7622bbb77696aae818f2f585a2dc8920",
              "name": "\u5f20\u7ff0\u5347"
            },
            "detail": [
              {
                "type": "str",
                "value": "\u6211\u64e6\uff0c\u741b\u54e5\u771f\u53f8\u673a"
              }
            ]
        },
#         "msg_id": "763692920983062415",
#         "msg_type_id": 3,
#         "to_user_id": "@1f55a89113749985d3d719997b86da3bd0b8730b94c46b49cab8bdc01f00bcaf",
#         "user": {
#             "id": "@@9601cb3ada4dd3e393df0ad1a73e69c18dbbb01ea5133b878a3b321700464e7a",
#             "name": "\u6253\u54cd\u6bd5\u4e1a\u6700\u540e\u4e00\u70ae"
#         }
    }
    print es.save_data('aaaaa', data=data)
    