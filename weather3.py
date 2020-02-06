import sys
from PySide2 import QtCore, QtScxml
import requests
import json
from datetime import datetime, timedelta, time

# 都道府県名のリスト
prefs = ['三重', '京都', '佐賀', '兵庫', '北海道', '千葉', '和歌山', '埼玉', '大分',
         '大阪', '奈良', '宮城', '宮崎', '富山', '山口', '山形', '山梨', '岐阜', '岡山',
         '岩手', '島根', '広島', '徳島', '愛媛', '愛知', '新潟', '東京',
         '栃木', '沖縄', '滋賀', '熊本', '石川', '神奈川', '福井', '福岡', '福島', '秋田',
         '群馬', '茨城', '長崎', '長野', '青森', '静岡', '香川', '高知', '鳥取', '鹿児島']

# 都道府県名から緯度と経度を取得するための辞書
latlondic = {'北海道': (43.06, 141.35), '青森': (40.82, 140.74), '岩手': (39.7, 141.15), '宮城': (38.27, 140.87),
             '秋田': (39.72, 140.1), '山形': (38.24, 140.36), '福島': (37.75, 140.47), '茨城': (36.34, 140.45),
             '栃木': (36.57, 139.88), '群馬': (36.39, 139.06), '埼玉': (35.86, 139.65), '千葉': (35.61, 140.12),
             '東京': (35.69, 139.69), '神奈川': (35.45, 139.64), '新潟': (37.9, 139.02), '富山': (36.7, 137.21),
             '石川': (36.59, 136.63), '福井': (36.07, 136.22), '山梨': (35.66, 138.57), '長野': (36.65, 138.18),
             '岐阜': (35.39, 136.72), '静岡': (34.98, 138.38), '愛知': (35.18, 136.91), '三重': (34.73, 136.51),
             '滋賀': (35.0, 135.87), '京都': (35.02, 135.76), '大阪': (34.69, 135.52), '兵庫': (34.69, 135.18),
             '奈良': (34.69, 135.83), '和歌山': (34.23, 135.17), '鳥取': (35.5, 134.24), '島根': (35.47, 133.05),
             '岡山': (34.66, 133.93), '広島': (34.4, 132.46), '山口': (34.19, 131.47), '徳島': (34.07, 134.56),
             '香川': (34.34, 134.04), '愛媛': (33.84, 132.77), '高知': (33.56, 133.53), '福岡': (33.61, 130.42),
             '佐賀': (33.25, 130.3), '長崎': (32.74, 129.87), '熊本': (32.79, 130.74), '大分': (33.24, 131.61),
             '宮崎': (31.91, 131.42), '鹿児島': (31.56, 130.56), '沖縄': (26.21, 127.68)}

current_weather_url = 'http://api.openweathermap.org/data/2.5/weather'
forecast_url = 'http://api.openweathermap.org/data/2.5/forecast'
appid = '' # 自身のAPPIDを入れてください

# テキストから都道府県名を抽出する関数．見つからない場合は空文字を返す．
def get_place(text):
    for pref in prefs:
        if pref in text:
            return pref
    return ""

# テキストに「今日」もしくは「明日」があればそれを返す．見つからない場合は空文字を返す．
def get_date(text):
    if "今日" in text:
        return "今日"
    elif "明日" in text:
        return "明日"
    else:
        return ""

# テキストに「天気」もしくは「気温」があればそれを返す．見つからない場合は空文字を返す．    
def get_type(text):
    if "天気" in text:
        return "天気"
    elif "気温" in text:
        return "気温"
    else:
        return ""

def get_current_weather(lat,lon):
    # 天気情報を取得    
    response = requests.get("{}?lat={}&lon={}&lang=ja&units=metric&APPID={}".format(current_weather_url,lat,lon,appid))
    return response.json()

def get_tomorrow_weather(lat,lon):
    # 今日の時間を取得
    today = datetime.today()
    # 明日の時間を取得
    tomorrow = today + timedelta(days=1)
    # 明日の正午の時間を取得
    tomorrow_noon = datetime.combine(tomorrow, time(12,0))
    # UNIX時間に変換
    timestamp = tomorrow_noon.timestamp()
    # 天気情報を取得
    response = requests.get("{}?lat={}&lon={}&lang=ja&units=metric&APPID={}".format(forecast_url,lat,lon,appid))
    dic = response.json()
    # 3時間おきの天気情報についてループ
    for i in range(len(dic["list"])):
        # i番目の天気情報（UNIX時間）
        dt = float(dic["list"][i]["dt"])
        # 明日の正午以降のデータになった時点でその天気情報を返す
        if dt >= timestamp:
            return dic["list"][i]
    return ""    

# Qtに関するおまじない
app = QtCore.QCoreApplication()
el  = QtCore.QEventLoop()

# SCXMLファイルの読み込み
sm  = QtScxml.QScxmlStateMachine.fromFile('states.scxml')

# 初期状態に遷移
sm.start()
el.processEvents()

# システムプロンプト
print("SYS> こちらは天気情報案内システムです")

# 状態とシステム発話を紐づけた辞書
uttdic = {"ask_place": "地名を言ってください",
          "ask_date": "日付を言ってください",
          "ask_type": "情報種別を言ってください"}

# 初期状態の取得
current_state = sm.activeStateNames()[0]
print("current_state=", current_state)

# 初期状態に紐づいたシステム発話の取得と出力
sysutt = uttdic[current_state]
print("SYS>", sysutt)

# ユーザ入力の処理
while True:
    text = input("> ")

    # ユーザ入力を用いて状態遷移
    if current_state == "ask_place":
        place = get_place(text)
        if place != "":
            sm.submitEvent("place")
            el.processEvents()
    elif current_state == "ask_date":
        date = get_date(text)
        if date != "":
            sm.submitEvent("date")
            el.processEvents()                   
    elif current_state == "ask_type":
        _type = get_type(text)
        if _type != "":
            sm.submitEvent("type")
            el.processEvents()                   

    # 遷移先の状態を取得
    current_state = sm.activeStateNames()[0]
    print("current_state=", current_state)

    # 遷移先がtell_infoの場合は情報を伝えて終了
    if current_state == "tell_info":
        print("お伝えします")
        lat = latlondic[place][0] # placeから緯度を取得
        lon = latlondic[place][1] # placeから経度を取得       
        print("lat=",lat,"lon=",lon)
        if date == "今日":
            cw = get_current_weather(lat,lon)
            if _type == "天気":
                print(cw["weather"][0]["description"]+"です")
            elif _type == "気温":
                print(str(cw["main"]["temp"])+"度です")
        elif date == "明日":
            tw = get_tomorrow_weather(lat,lon)
            if _type == "天気":
                print(tw["weather"][0]["description"]+"です")               
            elif _type == "気温":
                print(str(tw["main"]["temp"])+"度です")
        break
    else:
        # その他の遷移先の場合は状態に紐づいたシステム発話を生成
        sysutt = uttdic[current_state]
        print("SYS>", sysutt)           

# 終了発話
print("ご利用ありがとうございました")       

# end of file
