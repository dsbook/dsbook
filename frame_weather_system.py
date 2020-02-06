import sys
from da_concept_extractor import DA_Concept
import requests
import json
from datetime import datetime, timedelta, time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram_bot import TelegramBot

class FrameWeatherSystem:

    # 都道府県名のリスト
    prefs = ['三重', '京都', '佐賀', '兵庫', '北海道', '千葉', '和歌山', '埼玉', '大分',
             '大阪', '奈良', '宮城', '宮崎', '富山', '山口', '山形', '山梨', '岐阜', '岡山',
             '岩手', '島根', '広島', '徳島', '愛媛', '愛知', '新潟', '東京',
             '栃木', '沖縄', '滋賀', '熊本', '石川', '神奈川', '福井', '福岡', '福島', '秋田',
             '群馬', '茨城', '長崎', '長野', '青森', '静岡', '香川', '高知', '鳥取', '鹿児島']

    # 日付のリスト
    dates = ["今日","明日"]

    # 情報種別のリスト
    types = ["天気","気温"]    
    
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

    # システムの対話行為とシステム発話を紐づけた辞書
    uttdic = {"open-prompt": "ご用件をどうぞ",
              "ask-place": "地名を言ってください",
              "ask-date": "日付を言ってください",
              "ask-type": "情報種別を言ってください"}    

    current_weather_url = 'http://api.openweathermap.org/data/2.5/weather'
    forecast_url = 'http://api.openweathermap.org/data/2.5/forecast'
    appid = '' # 自身のAPPIDを入れてください    
    
    def __init__(self):
        # 対話セッションを管理するための辞書
        self.sessiondic = {}
        # 対話行為タイプとコンセプトを抽出するためのモジュールの読み込み
        self.da_concept = DA_Concept()
    
    def get_current_weather(self, lat,lon):
        # 天気情報を取得    
        response = requests.get("{}?lat={}&lon={}&lang=ja&units=metric&APPID={}".format(self.current_weather_url,lat,lon,self.appid))
        return response.json()

    def get_tomorrow_weather(self, lat,lon):
        # 今日の時間を取得
        today = datetime.today()
        # 明日の時間を取得
        tomorrow = today + timedelta(days=1)
        # 明日の正午の時間を取得
        tomorrow_noon = datetime.combine(tomorrow, time(12,0))
        # UNIX時間に変換
        timestamp = tomorrow_noon.timestamp()
        # 天気情報を取得
        response = requests.get("{}?lat={}&lon={}&lang=ja&units=metric&APPID={}".format(self.forecast_url,lat,lon,self.appid))
        dic = response.json()
        # 3時間おきの天気情報についてループ
        for i in range(len(dic["list"])):
            # i番目の天気情報（UNIX時間）
            dt = float(dic["list"][i]["dt"])
            # 明日の正午以降のデータになった時点でその天気情報を返す
            if dt >= timestamp:
                return dic["list"][i]
        return ""

    # 発話から得られた情報をもとにフレームを更新
    def update_frame(self, frame, da, conceptdic):
        # 値の整合性を確認し，整合しないものは空文字にする
        for k,v in conceptdic.items():
            if k == "place" and v not in self.prefs:
                conceptdic[k] = ""
            elif k == "date" and v not in self.dates:
                conceptdic[k] = ""
            elif k == "type" and v not in self.types:
                conceptdic[k] = ""
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

    # フレームの状態から次のシステム対話行為を決定
    def next_system_da(self, frame):
        # すべてのスロットが空であればオープンな質問を行う
        if frame["place"] == "" and frame["date"] == "" and frame["type"] == "":
            return "open-prompt"
        # 空のスロットがあればその要素を質問する
        elif frame["place"] == "":
            return "ask-place"
        elif frame["date"] == "":
            return "ask-date"
        elif frame["type"] == "":
            return "ask-type"
        else:
            return "tell-info"

    def initial_message(self, input):
        text = input["utt"]
        sessionId = input["sessionId"]

        # セッションIDとセッションに関連する情報を格納した辞書
        self.sessiondic[sessionId] = {"frame": {"place": "", "date": "", "type": ""}}

        return {"utt":"こちらは天気情報案内システムです。ご用件をどうぞ。", "end":False}

    def reply(self, input):
        text = input["utt"]
        sessionId = input["sessionId"]

        # 現在のセッションのフレームを取得
        frame = self.sessiondic[sessionId]["frame"]
        print("frame=", frame)

        # 発話から対話行為タイプとコンセプトを取得
        da, conceptdic = self.da_concept.process(text)
        print(da, conceptdic)

        # 対話行為タイプとコンセプトを用いてフレームを更新
        frame = self.update_frame(frame, da, conceptdic)
        print("updated frame=", frame)

        # 更新後のフレームを保存
        self.sessiondic[sessionId] = {"frame": frame}

        # フレームからシステム対話行為を得る
        sys_da = self.next_system_da(frame)

        # 遷移先がtell-infoの場合は情報を伝えて終了
        if sys_da == "tell-info":
            utts = []
            utts.append("お伝えします")
            place = frame["place"]
            date = frame["date"]
            _type = frame["type"]

            lat = self.latlondic[place][0] # placeから緯度を取得
            lon = self.latlondic[place][1] # placeから経度を取得       
            print("lat=",lat,"lon=",lon)
            if date == "今日":
                cw = self.get_current_weather(lat,lon)
                if _type == "天気":
                    utts.append(cw["weather"][0]["description"]+"です")
                elif _type == "気温":
                    utts.append(str(cw["main"]["temp"])+"度です")
            elif date == "明日":
                tw = self.get_tomorrow_weather(lat,lon)
                if _type == "天気":
                    utts.append(tw["weather"][0]["description"]+"です")
                elif _type == "気温":
                    utts.append(str(tw["main"]["temp"])+"度です")
            utts.append("ご利用ありがとうございました")
            del self.sessiondic[sessionId]
            return {"utt":"。".join(utts), "end": True}

        else:
            # その他の遷移先の場合は状態に紐づいたシステム発話を生成
            sysutt = self.uttdic[sys_da]            
            return {"utt":sysutt, "end": False}

if __name__ == '__main__':
    system = FrameWeatherSystem()
    bot = TelegramBot(system)
    bot.run()    

# end of file
