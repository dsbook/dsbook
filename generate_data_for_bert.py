import random

write_lines = []
uttrs = []

with open("dialogue_pairs.txt") as f:
    for l in f:
        if "\t" in l:
            l = l.strip()
            # 実際の応答ペアを正解とし，ラベルは1とする．
            write_lines.append(l + "\t1\n")
            # 不正解ペアの作成のため，発話を保存
            uttrs.append(l.split("\t")[0])
            uttrs.append(l.split("\t")[1])
  
# 正解ペアと同じ数だけ不正解ペアを作成
for i in range(len(write_lines)):
    # ランダムな応答ペアを不正解とし，ラベルは0とする．
    write_lines.append(random.choice(uttrs) + "\t" + random.choice(uttrs) + "\t0\n")
  
 # 正解ペアと不正解ペアが入ったリストをシャッフルする
random.shuffle(write_lines)
  
index = 0
with open("dev.tsv", "w") as var_f:
    # 開発データとしてdev.tsvに200行を書き込む．
    for l in write_lines[:200]:
        var_f.write(str(index) + "\t" + l)
        index += 1
index = 0
with open("train.tsv", "w") as var_f:
    # 学習データとしてtrain.tsvにのこりを書き込む．
    for l in write_lines[200:]:
        var_f.write(str(index) + "\t" + l)
        index += 1
        
