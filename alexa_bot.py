from flask import Flask
from flask_ask import Ask, statement, question, session
import ebdm_system

# Flaskを起動
app = Flask(__name__)
ask = Ask(app, '/')

# 対話システムを起動
system = ebdm_system.EbdmSystem()

# alexaから送られてきたテキストのうち，最も長いもの（＝ユーザの発話）を抜き出すためのメソッド
def marge_texts(texts):
    text = ''
    for t in texts:
        try:
            if len(t) >= len(text):
                text = t
        except: pass
    return text

# 起動した時に呼び出されるインテント
@ask.launch
def launch():
    # 発話はなし，session.sessionIdでセッションIDを取得してinitial_messageを返答
    response = system.initial_message({"utt":"","sessionId":session.sessionId})
    return question(response['utt'])

# ユーザが話しかけた時に呼び出されるインテント
# mappingはalexaから送られてきたスロット（情報）をどのような変数名で受け取るかを定義している
@ask.intent('HelloIntent', mapping={'any_text_a': 'any_text_a', 'any_text_b': 'any_text_b','any_text_c': 'any_text_c', })
def talk(any_text_a, any_text_b, any_text_c):
#   受け取ったスロットをまとめて，長いものを抜き出す
    texts = [ any_text_a, any_text_b, any_text_c ]
    text = marge_texts(texts)
#   ユーザ発話を対話システムの応答生成に与える，セッションIDもsession.sessionIdで取得する
    mes = system.reply({"utt":text,"sessionId":session.sessionId})

#   この発話で終了する時はstatement（この発話でスキルを終了する）で応答
    if mes['end']: return statement(mes['utt'])
#   この発話で終了しない場合はquestion（ユーザの応答を待つ）で応答
    else: return question(mes['utt'])

if __name__ == '__main__':
#   port8080でflaskのサーバを起動
    app.run(port=8080)
