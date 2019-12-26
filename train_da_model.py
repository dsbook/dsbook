import MeCab
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import dill 

# MeCabの初期化
mecab = MeCab.Tagger()
mecab.parse('')

sents = []
labels = []

# generate-samples.txt の出力である samples.dat の読み込み
for line in open("da_samples.dat","r"):
    line = line.rstrip()
    # samples.dat は対話行為タイプ，発話文，タグとその文字位置が含まれている
    da, utt = line.split('\t')
    words = []
    for line in mecab.parse(utt).splitlines():
        if line == "EOS":
            break
        else:
            # MeCabの出力から単語を抽出
            word, feature_str = line.split("\t")
            words.append(word)
    # 空白区切りの単語列をsentsに追加
    sents.append(" ".join(words))
    # 対話行為タイプをlabelsに追加
    labels.append(da)

# TfidfVectorizerを用いて，各文をベクトルに変換
vectorizer = TfidfVectorizer(tokenizer=lambda x:x.split(), ngram_range=(1,3))
X = vectorizer.fit_transform(sents)

# LabelEncoderを用いて，ラベルを数値に変換
label_encoder = LabelEncoder()
Y = label_encoder.fit_transform(labels)

# SVMでベクトルからラベルを取得するモデルを学習
svc = SVC(gamma="scale")
svc.fit(X,Y)

# 学習されたモデル等一式を svc.modelに保存
with open("svc.model","wb") as f:
    dill.dump(vectorizer, f)
    dill.dump(label_encoder, f)
    dill.dump(svc, f)

