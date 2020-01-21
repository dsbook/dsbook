import MeCab
import os

# データ数を設定
TRAIN_PAIR_NUM = 500000
DEV_PAIR_NUM = 2000
TEST_PAIR_NUM = 2000

mecab = MeCab.Tagger ("-Owakati")
mecab.parse("")
 
source = []
target = []
with open("tweet_pairs.txt") as f:
    for i, line in enumerate(f):
        line = line.strip()

        if "\t" in line:
            s = mecab.parse(line.rsplit("\t", 1)[0].replace("\t", " SEP "))
            t = mecab.parse(line.rsplit("\t", 1)[1])
            # 両方とも5単語以上のツイートリプライペアを使用
            if len(s) >= 5 and len(t) >= 5:
                source.append(s)
                target.append(t)
        # 設定したデータ数に達したら読み込みを終了
        if len(source) > DEV_PAIR_NUM + TEST_PAIR_NUM + TRAIN_PAIR_NUM:
            break

# 出力用のディレクトリを作成
os.makedirs("OpenNMT", exist_ok=True)

# ファイル出力
with open("OpenNMT/dev.src", "w") as f:
    for l in source[0:DEV_PAIR_NUM]:
        f.write(l)
with open("OpenNMT/dev.tgt", "w") as f:
    for l in target[0:DEV_PAIR_NUM]:
        f.write(l)
with open("OpenNMT/test.src", "w") as f:
    for l in source[DEV_PAIR_NUM:DEV_PAIR_NUM + TEST_PAIR_NUM]:
        f.write(l)
with open("OpenNMT/test.tgt", "w") as f:
    for l in target[DEV_PAIR_NUM:DEV_PAIR_NUM + TEST_PAIR_NUM]:
        f.write(l)
with open("OpenNMT/train.src", "w") as f:
    for l in source[DEV_PAIR_NUM + TEST_PAIR_NUM:DEV_PAIR_NUM + TEST_PAIR_NUM + TRAIN_PAIR_NUM]:
        f.write(l)
with open("OpenNMT/train.tgt", "w") as f:
    for l in target[DEV_PAIR_NUM + TEST_PAIR_NUM:DEV_PAIR_NUM + TEST_PAIR_NUM + TRAIN_PAIR_NUM]:
        f.write(l)
