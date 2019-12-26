import random

# システムの対話行為
sys_da_lis = [
    "open-prompt",
    "ask-place",
    "ask-date",
    "ask-type",
    "tell-info"]

# システムの状態
states = ["000","001","010","011","100","101","110","111"]

# Q値（行動状態価値）の初期化
Q = {}
for state in states:
    Q[state] = {}
    for sys_da in sys_da_lis:
        Q[state][sys_da] = 0

# フレームを更新        
def update_frame(frame, da, conceptdic):
    if da == "request-weather":
        for k,v in conceptdic.items():
            # コンセプトの情報でスロットを埋める
            frame[k] = v
    elif da == "initialize":
        frame = {"place": "", "date": "", "type": ""}
    elif da == "correct-info":
        for k,v in conceptdic.items():
            if frame[k] == v:
                frame[k] = ""
    return frame

# フレームから状態を表す文字列に変換
# place, date, type の順に値が埋まっていたら1，埋まってなければ0
def frame2state(frame):
    state = ""
    for k in ["place","date","type"]:
        if frame[k] == "":
            state += "0"
        else:
            state += "1"            
    return state

# ユーザシミュレータ
# ユーザは聞かれたスロットについて的確に答える．
# open-promptには聞きたいことをいくつかランダムに伝える．
# tell-info によるシステム回答の内容が合っていたらgoodbyeをする．
# tell-infoの内容が間違っていたらinitializeをする．
def next_user_da(sys_da, sys_conceptdic, intention):
    if sys_da == "ask-place":
        return "request-weather", {"place": intention["place"]}
    elif sys_da == "ask-date":
        return "request-weather", {"date": intention["date"]}
    elif sys_da == "ask-type":
        return "request-weather", {"type": intention["type"]}
    elif sys_da == "open-prompt":
        while(True):
            dic = {}
            for k,v in intention.items():
                if random.choice([0,1]) == 0:
                    dic[k] = v
            if len(dic) > 0:
                return "request-weather", dic
    elif sys_da == "tell-info":
        is_ok = True
        for k,v in intention.items():
            if sys_conceptdic[k] != v:
                is_ok = False
                break
        if is_ok:
            return "goodbye", {}
        else:
            return "initialize", {}

# ランダムに行動
def next_system_da(frame):
    # 値がすべて埋まってないとtell-infoは発話できない
    cands = list(sys_da_lis)
    if frame["place"] == "" or frame["date"] == "" or frame["type"] == "":
        cands.remove("tell-info")        
    value = random.random()
    sys_da = random.choice(cands)
    sys_conceptdic = {}
    if sys_da == "tell-info":
        sys_conceptdic = frame
    return sys_da, sys_conceptdic

# 対話を成功するまで一回実行
# intentionはユーザの意図，alphaは学習係数，gammaは割引率を表す
def run_dialogue(intention, alpha=0.1, gamma=0.9):
    frame = {"place": "", "date": "", "type": ""}
    while(True):
        s1 = frame2state(frame)
        sys_da, sys_conceptdic = next_system_da(frame)
        da, conceptdic = next_user_da(sys_da, sys_conceptdic, intention)
        frame = update_frame(frame, da, conceptdic)
        s2 = frame2state(frame)
        # 遷移先の状態（s2）から得られる最大の価値を取得
        da_lis = sorted(Q[s2].items(),key=lambda x:x[1], reverse=True)
        maxval = da_lis[0][1]
        if da == "goodbye":
            # 成功した対話の後の状態は存在しないのでmaxvalは0
            maxval = 0
            # Q値を更新して対話を終わる
            Q[s1][sys_da] = Q[s1][sys_da] + alpha * ((100 + gamma * maxval) - Q[s1][sys_da])
            break
        else:
            # Q値を更新
            Q[s1][sys_da] = Q[s1][sys_da] + alpha * ((0 + gamma * maxval) - Q[s1][sys_da])

if __name__ == "__main__":
    # 千回対話をして学習
    for i in range(100000):
        run_dialogue({"place":"大阪","date":"明日","type":"天気"})
    # Q値を表示
    print(Q)
    # 各状態で最適な行動をQ値とともに表示
    for k,v in Q.items():
        da_lis = sorted(Q[k].items(),key=lambda x:x[1], reverse=True)
        print(k, "=>", da_lis[0][0], da_lis[0][1])

# end of file    
