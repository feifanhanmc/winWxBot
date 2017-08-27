# -*- coding: utf-8 -*-
'''
Relational DB -> Databases -> Tables -> Rows          -> Columns
Elasticsearch -> Indices       ->  Types -> Documents -> Fields

'''
import json
from elasticsearch import Elasticsearch


class ES():
    def __init__(self, host='hanmengcheng.com:9200', index_name='wxbot_index', doc_type='msg_text'):
        self.es = Elasticsearch(host)
        self.index_name = index_name
        self.doc_type = doc_type

    def create_index(self, index_name=None):
        #create a index without replicas 
        if index_name:
            self.index_name = index_name
        self.es.indices.create(index=self.index_name, ignore=400, body={
            "index" : {
                "number_of_replicas" : 0
            }
        })
    
    def save_data(self, msg, doc_type=None):
        '''
        :param msg(dict)
        '''
        if doc_type:
            self.doc_type = doc_type
        self.es.index(index=self.index_name, doc_type=self.doc_type, id=msg['msg_id'], body=json.JSONEncoder().encode(msg))
            
    

if __name__ == '__main__':
    es = ES()


