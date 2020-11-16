class ConsoleBot:
    def __init__(self, system):
        self.system = system
 
    def start(self, input_utt):
        # 辞書型 inputにユーザIDを設定
        input = {'utt': None, 'sessionId': "myid"}
 
        # システムからの最初の発話をinitial_messageから取得し，送信
        return self.system.initial_message(input)
 
    def message(self, input_utt):
        # 辞書型 inputにユーザからの発話とユーザIDを設定
        input = {'utt': input_utt, 'sessionId': "myid"}
 
        # replyメソッドによりinputから発話を生成
        system_output = self.system.reply(input)
 
        # 発話を送信
        return system_output
 
    def run(self):
        while True:
            input_utt = input("YOU:>")
            if "/start" in input_utt:
                sys_out = self.start(input_utt)
            else:
                sys_out = self.message(input_utt)
            print("SYS:" + sys_out["utt"])

            if sys_out["end"]:
                break