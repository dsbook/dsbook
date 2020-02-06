from telegram_bot import TelegramBot
import weather_system
import ebdm_system

class IntegrationSystem1:
    def __init__(self):
        # 二つのシステムを初期化する
        self.system1 = weather_system.WeatherSystem()
        self.system2 = ebdm_system.EbdmSystem()

    def initial_message(self, input):
        # システムを全て初期化する
        output = self.system1.initial_message(input)
        self.system2.initial_message(input)
        return output
        
    def reply(self, input):
        # 特定のキーワードが入っていたら，system1を，それ以外の場合はsystem2を呼びだす
        if '天気' in input['utt']:
            output = self.system1.reply(input)
            if output['end']:
                # もし天気予報が完了していたら，再度初期化する
                self.system1.initial_message(input)
        else:
            output = self.system2.reply(input)
        return output

if __name__ == '__main__':
    system = IntegrationSystem1()
    bot = TelegramBot(system)
    bot.run()
