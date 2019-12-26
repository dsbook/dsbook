import json
import dill
import sklearn_crfsuite
from crf_util import word2features, sent2features, sent2labels

sents = []
lis = []

# concept_samples.dat の読み込み
for line in open("concept_samples.dat","r"):
    line = line.rstrip()
    # 空行で一つの事例が完了
    if line == "":
        sents.append(lis)
        lis = []
    else:
        # concept_samples.dat は単語，品詞，ラベルがタブ区切りになっている
        word, postag, label = line.split('\t')
        lis.append([word, postag, label])

# 各単語の情報を素性に変換
X = [sent2features(s) for s in sents]

# 各単語のラベル情報
Y = [sent2labels(s) for s in sents]

# CRFによる学習
crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=False
)
crf.fit(X, Y)

# CRFモデルの保存
with open("crf.model","wb") as f:
    dill.dump(crf, f)

