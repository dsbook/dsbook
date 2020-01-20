from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram_bot import TelegramBot
 
# ユーザの入力をそのまま返す対話システム．
class EchoSystem:
    def __init__(self):
        pass
 
    def initial_message(self, input):
        return {'utt': 'こんにちは。対話を始めましょう。', 'end':False}
 
    def reply(self, input):
        return {"utt": input['utt'], "end": False}
 
 
if __name__ == '__main__':
    system = EchoSystem()
    bot = TelegramBot(system)
    bot.run()
    
