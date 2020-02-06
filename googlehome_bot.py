import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import ebdm_system

# 対話システムを起動
system = ebdm_system.EbdmSystem()

# Dialogflowからの情報を受け取るサーバのクラス
class MyHandler(BaseHTTPRequestHandler):
#   dialogflowから情報が送られてきた時にこのメソッドが呼び出される
    def do_POST(self):
        try:
            # 送られてきた情報を取得
            content_len=int(self.headers.get('content-length'))
            requestBody = json.loads(self.rfile.read(content_len).decode('utf-8'))
#           dialogflowから送られてきた情報から，ユーザの発話と対話のセッションIDを抜き出す
            input = {}
            input['utt'] = requestBody['queryResult']['queryText']
            input['sessionId'] = requestBody['session']

            if requestBody['queryResult']['queryText'] == 'GOOGLE_ASSISTANT_WELCOME':
#               welcome intentの時はinitial_messageを呼び出して最初のメッセージを取得
                output = system.initial_message(input)
            else:
#               それ以外の時はreplyを呼び出して応答を取得
                output = system.reply(input)

#           dialogflowに応答文を送り返す
            response = { 'status' : 200,
                         'fulfillmentText': output['utt']
                        }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            responseBody = json.dumps(response)
            self.wfile.write(responseBody.encode('utf-8'))

        except Exception as e:
#           エラーが発生した時
            response = { 'status' : 500,
                         'msg' : 'An error occured' }
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            responseBody = json.dumps(response)
            self.wfile.write(responseBody.encode('utf-8'))


# サーバを起動するメソッド
def run(server_class=HTTPServer, handler_class=MyHandler, server_name='localhost', port=8080):
    server = server_class((server_name, port), handler_class)
    server.serve_forever()

if __name__ == '__main__':
    run()
