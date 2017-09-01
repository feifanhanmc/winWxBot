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
        return self.es.index(index=self.index_name, doc_type=doc_type, body=json.dumps(data), id=data_id)
        
    
if __name__ == '__main__':
#     es = WX_XNR_ES()
    with open('wx_xnr_conf.json', 'r') as f:
        config = json.load(f)
    wx_xnr_groupmsg = {'msg_type':'text','group_name':u'group001','speaker_name':u'\u97e9\u68a6\u6210','date':'2017-09-01','group_id':u'@@f16477692f4369fd402fe29b665a9ac482a2ca0f1f2fb3cf26daaa5e1569491f','data':{'str':u'\u6d4b\u8bd5'},'speaker_id':u'@4e6013041060394ab29bb4f04402aa854d1f11ff874c39d2a5534f9701f930c4'}    
    WX_XNR_ES(host=config['es_host'], index_name=config['es_index_name']).save_data(doc_type='groupmsg', data=wx_xnr_groupmsg)