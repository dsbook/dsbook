from telegram_bot import TelegramBot
from elasticsearch import Elasticsearch
import MeCab
# コサイン類似度で使うライブラリ
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
# レーベンシュタイン距離で使うライブラリ
import Levenshtein
# word mover's distanceで使うライブラリ
from gensim.models import Word2Vec
tagger = MeCab.Tagger('-Owakati')
tagger.parse("")
try:
    w2v = Word2Vec.load('./word2vec.gensim.model')
except:
    pass

# 類似度の評価関数
# コサイン類似度
def cosine(a, b):
    # 2章で発話のベクトル化をした時と同じように，sklearnのvectorizerを使って単語頻度ベクトルを作る
    a, b = CountVectorizer(token_pattern=u'(?u)\\b\\w+\\b').fit_transform([tagger.parse(a), tagger.parse(b)])
    # cosine_similarityでコサイン類似度を計算する
    return cosine_similarity(a, b)[0]

# レーベンシュタイン距離
def levenshtein(a, b):
    # Levenshtein距離を計算する，これは距離なので-をつける
    return -Levenshtein.distance(a, b)

# word mover's distance
def wmd(a, b):
    # mecabで単語に区切る
    a, b = tagger.parse(a).split(), tagger.parse(b).split()
    # word mover's distanceを計算する
    return -w2v.wmdistance(a, b)

class EbdmSystem:
    def __init__(self):
        self.es = Elasticsearch()

    def initial_message(self, input):
        return {'utt': 'こんにちは。対話を始めましょう。', 'end':False}
    
    def reply(self, input):
        max_score = -float('inf')
        result = ''

        for r in self.__reply(input['utt']):
            score = self.evaluate(input['utt'], r)
            if score > max_score:
                max_score = score
                result = r[1]
        return {"utt": result, "end": False}

    def __reply(self, utt):
        results = self.es.search(index='dialogue_pair',
                    body={'query':{'match':{'query':utt}}, 'size':100,})
        return [(result['_source']['query'], result['_source']['response'], result["_score"]) for result in results['hits']['hits']]
        
    def evaluate(self, utt, pair):
        #utt:     ユーザ発話
        #pair[0]: 用例ベースのtweet
        #pair[1]: 用例ベースのreply
        #pair[2]: elasticsearchのスコア
        #返り値:  評価スコア（大きいほど応答として適切）
        return pair[2]

if __name__ == '__main__':
    system = EbdmSystem()
    bot = TelegramBot(system)
    bot.run()
