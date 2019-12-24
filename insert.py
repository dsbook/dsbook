from elasticsearch import Elasticsearch, helpers
es = Elasticsearch()
# tsvから読み出してinsertするバージョンに変更→済み

def load():
    with open('./dialogue_pairs.txt') as f:
        for i, __ in enumerate(f):
            print(i, '...', end='\r')
            __ = __.split('\t')
            tweet = __[0].strip()
            reply = __[1].strip()
            item = {'_index':'dialogue_pair', '_type':'docs', '_source':{ 'query':tweet, 'response':reply }}
            yield item

if __name__ == '__main__':
    print(helpers.bulk(es, load()))

