from telegram_bot import TelegramBot
import weather_system
import ebdm_system

class IntegrationSystem2:
    def __init__(self):
        # 二つのシステムを初期化する
        self.system1 = weather_system.WeatherSystem()
        self.system2 = ebdm_system.EbdmSystem()
        self.sessiondic = {}

    def initial_message(self, input):
        sessionId = input['sessionId']
        # システムを全て初期化する
        output = self.system1.initial_message(input)
        self.system2.initial_message(input)
        self.sessiondic[sessionId] = output['utt']
        return output
        
    def reply(self, input):
        sessionId = input['sessionId']
        # まずはタスク対話の結果を取得する
        output = self.system1.reply(input)

        print(self.sessiondic[sessionId])
        print(output)
        # タスク対話が進みそう（前の発話と違う内容に）でなければ，雑談対話を行う
        if output['utt'] == self.sessiondic[sessionId]:
            output = self.system2.reply(input)
        else:
            # タスク対話が進んだ場合は，その発話を覚えておく
            self.sessiondic[sessionId] = output['utt']
            # タスク対話が終了していたら，再度初期化する
            if output['end']:
                self.system1.initial_message(input)

        return output

if __name__ == '__main__':
    system = IntegrationSystem2()
    bot = TelegramBot(system)
    bot.run()
