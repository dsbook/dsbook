import zipfile
import json
import glob
import os


def annotations_to_o_ratio(annotations):
    o_count = 0
    t_count = 0
    x_count = 0
    for a in annotations:
        if a["breakdown"] == "O":
            o_count += 1
        elif a["breakdown"] == "T":
            t_count += 1
        elif a["breakdown"] == "X":
            x_count += 1
    o_ratio = 0.0
    if o_count > 0:
        o_ratio = o_count / (o_count + t_count + x_count)
    return str(o_ratio)


write_lines = []
# 同じディレクトリ内のzipファイルをすべて読み込み
for f in glob.glob("DBDC2*.zip"):
    with zipfile.ZipFile(f, 'r') as z:
        features = []
        # zipファイル内のjsonファイルをすべて読み込み
        for filename in z.namelist():
            if "json" in filename:
                with z.open(filename) as f:
                    data = f.read()
                    # JSONデータの読み込み
                    json_data = json.loads(data.decode("utf-8"))

                    uttr_logs = []
                    for d in json_data["turns"]:
                        feature = []
                        uttr_logs.append(d["utterance"])
                        if d["speaker"] is "S" and len(uttr_logs) > 2:
                            write_lines.append(uttr_logs[-2] + "\t" + uttr_logs[-1] + "\t" + annotations_to_o_ratio(d["annotations"]))

# 出力用のディレクトリを作成
os.makedirs("dbdc_bert", exist_ok=True)


with open("dbdc_bert/dev.tsv", "w") as var_f:
    var_f.write("\n")
    for l in write_lines[:200]:
        var_f.write("\t\t\t\t\t\t\t" + l + "\n")

with open("dbdc_bert/train.tsv", "w") as var_f:
    var_f.write("\n")
    for l in write_lines[200:]:
        var_f.write("\t\t\t\t\t\t\t" + l + "\n")
