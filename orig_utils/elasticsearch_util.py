#!/usr/bin/python

from elasticsearch import Elasticsearch
from datetime import datetime

class ElasticSearchHandler(object):
    def __init__(self):
        self.es = Elasticsearch()
        self.rec_id = 0

    def add_record(self,rec_dict,db_index,rec_doc_type):
        self.rec_id+=1
        res = self.es.index(index=db_index,
                       doc_type=rec_doc_type,
                       id=self.rec_id,
                       body=rec_dict)
        return(res['ok'])

    def _search(self,db_index):
        self.es.indices.refresh(index=db_index)

        res = self.es.search(index=db_index,
                             body={"query": {"match_all": {}}})
        return(res)
        
    def search(self,db_index):
        res = self._search(db_index)
               
        print("Got %d Hits:" % res['hits']['total'])
        for hit in res['hits']['hits']:
            print hit["_source"]
            print("%(absname)s" % hit["_source"])

        print res.keys()

if __name__ == '__main__':    
    doc = {
        'author': 'kimchy',
        'text': 'Elasticsearch: cool. bonsai cool.',
        'timestamp': datetime(2011, 10, 10, 10, 10, 10)
    }

    doc2 = {
        'author': 'burtnolej',
        'text': 'Elasticsearch: cool. bonsai cool.',
        'timestamp': datetime(2011, 10, 10, 10, 10, 10)
    }

    #res = es.get(index="test-index", doc_type='tweet', id=1)
    #print(res['_source'])


    #es.indices.refresh(index="test-index")

    #res = es.search(index="test-index", body={"query": {"match_all": {}}})
    #print("Got %d Hits:" % res['hits']['total'])
    #for hit in res['hits']['hits']:
    #    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])



    es = ElasticSearchHandler()
    es.add_record(doc,'test-index','tweet')
    es.add_record(doc2,'test-index','tweet')
    #es.add_record(doc,'test-index','tweet',1)
    es.search('test-index')
