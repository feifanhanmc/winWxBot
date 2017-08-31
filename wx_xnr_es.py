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
        return self.es.indices.create(index=self.index_name, ignore=400, body={
            'settings':{
                'number_of_shards':5,
                'number_of_replicas':0,
            },
            'mappings':mappings
        })
    
    def create_doc_type(self, doc_type, mapping={}, index_name=None):
        #实际上是通过put_mapping的方式规定一个doc_type的mapping，但实际上有些不符合该mapping的数据也能存储进来，并改变mapping
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
#     es.create_index()
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
#     es.create_doc_type('test', mapping=test_mapping)
    print es.save_data('test', data={'m':'ssss','msg_id':'4444'})
    