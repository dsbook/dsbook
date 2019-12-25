import weather_system
import ebdm_system

class IntegrationSystem2:
    def __init__(self):
        # 二つのシステムを初期化する
        self.system1 = weather_system.AimlSystem()
        self.system2 = ebdm_system.EbdmSystem()

    def initial_message(self, input):
        # システムを全て初期化する
        self.system1.initial_message(input)
        self.system2.initial_message(input)
        return {'utt':'こんにちは。対話を始めましょう。', 'end':False}
        
    def reply(self, input):
        # まずはタスク対話の結果を取得する
        output = self.system1.reply(input)
        # タスク対話が進みそうでなければ，雑談対話を行う
        if output['utt'] == 'もう一度言ってください':
            return self.system2.reply(input)
        else:
            return output

if __name__ == '__main__':
    systems = IntegrationSystem2()
    print("SYS> " + systems.initial_message({'utt': '', 'sessionId': ''})['utt'])
    while 1:
        text = input("> ")
        print("SYS> " + systems.reply({'utt': text, 'sessionId': ''})['utt'])
