import sys
import aiml
import MeCab

class AimlSystem:
    def __init__(self):
        # AIMLを読み込むためのライブラリを用意
        self.kernel = aiml.Kernel()
        # aiml.xmlを読み込む
        self.kernel.learn("aiml.xml")
        # 形態素解析器を用意
        self.tagger = MeCab.Tagger('-Owakati')
        
    def initial_message(self, utt):
        return {'utt':'はじめまして，雑談を始めましょう', 'sessionId':'dummy'}

    def reply(self, utt):
        utt = utt['utt']
        utt = self.tagger.parse(utt)
        # kernel.respondでマッチするルールを探す
        return {'utt': self.kernel.respond(utt), 'end':False}
        
if __name__ == '__main__':
    aiml = AimlSystem()
    print("SYS> " + aiml.initial_message({'utt': '', 'sessionId': ''})['utt'])
    while 1:
        text = input("> ")
        print("SYS> " + aiml.reply({'utt': text, 'sessionId': ''})['utt'])
