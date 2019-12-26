import sys
from PySide2 import QtCore, QtScxml

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
   sm.submitEvent(text)
   el.processEvents()
   
   # 遷移先の状態を取得
   current_state = sm.activeStateNames()[0]
   print("current_state=", current_state)
   
   # 遷移先がtell_infoの場合は情報を伝えて終了
   if current_state == "tell_info":
       print("天気をお伝えします")       
       break
   else:
       # その他の遷移先の場合は状態に紐づいたシステム発話を生成
       sysutt = uttdic[current_state]
       print("SYS>", sysutt)           

# 終了発話
print("ご利用ありがとうございました")       

# end of file
