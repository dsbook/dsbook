import sys
from bert_evaluator import BertEvaluator
from telegram_bot import TelegramBot

class BertEbdmSystem:
    def __init__(self):
        from elasticsearch import Elasticsearch
        self.es = Elasticsearch()
        self.evaluator = BertEvaluator()

    def initial_message(self, input):
        return {'utt': 'こんにちは。対話を始めましょう。', 'end':False}
    
    def reply(self, input):
        max_score = .0
        result = ''

        for r in self.__reply(input['utt']):
            score = self.evaluate(input['utt'], r)
            if score >= max_score:
                max_score = score
                result = r[1]
        return {"utt": result, "end": False}

        
    def __reply(self, utt):
        results = self.es.search(index='dialogue_pair',
                    body={'query':{'match':{'query':utt}}, 'size':10,})
        return [(result['_source']['query'], result['_source']['response'], result["_score"]) for result in results['hits']['hits']]

        
    def evaluate(self, utt, pair):
        return self.evaluator.evaluate(utt, pair[1])
    
if __name__ == '__main__':
    system = BertEbdmSystem()
    bot = TelegramBot(system)
    bot.run()

