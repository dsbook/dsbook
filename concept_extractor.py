import MeCab
import json
import dill
import sklearn_crfsuite
from crf_util import word2features, sent2features, sent2labels
import re

# MeCabの初期化
mecab = MeCab.Tagger()
mecab.parse('')

# CRFモデルの読み込み
with open("crf.model","rb") as f:
    crf = dill.load(f)
    
# 発話文からコンセプトを抽出
def extract_concept(utt):
    lis = []
    for line in mecab.parse(utt).splitlines():
        if line == "EOS":
            break
        else:
            word, feature_str = line.split("\t")
            features = feature_str.split(',')
            postag = features[0]
            lis.append([word, postag, "O"])

    words = [x[0] for x in lis]            
    X = [sent2features(s) for s in [lis]]
    
    # 各単語に対応するラベル列
    labels = crf.predict(X)[0]
    
    # 単語列とラベル系列の対応を取って辞書に変換
    conceptdic = {}
    buf = ""
    last_label = ""
    for word, label in zip(words, labels):
        if re.search(r'^B-',label):
            if buf != "":
                _label = last_label.replace('B-','').replace('I-','')
                conceptdic[_label] = buf                    
            buf = word
        elif re.search(r'^I-',label):
            buf += word
        elif label == "O":
            if buf != "":
                _label = last_label.replace('B-','').replace('I-','')
                conceptdic[_label] = buf
                buf = ""
        last_label = label
    if buf != "":
        _label = last_label.replace('B-','').replace('I-','')
        conceptdic[_label] = buf
        
    return conceptdic

if __name__ ==  '__main__':
    for utt in ["大阪の明日の天気","もう一度はじめから","東京じゃなくて"]:    
        conceptdic = extract_concept(utt)
        print(utt, conceptdic)
