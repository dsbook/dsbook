import sys
import aiml
import MeCab
# replyに送るuttの形式がdictになっていないので修正→済
# initial_message関数がない→済み
class AimlSystem:
    def __init__(self):
        self.kernel = aiml.Kernel()
        self.kernel.learn("aiml.xml")
        self.tagger = MeCab.Tagger('-Owakati')
        
    def initial_message(self, utt):
        return {'utt':'はじめまして，雑談を始めましょう', 'sessionId':'dummy'}

    def reply(self, utt):
        utt = utt['utt']
        utt = self.tagger.parse(utt)
        return self.kernel.respond(utt)
        
if __name__ == '__main__':
    aimlessly = AimlSystem()
    while 1:
        text = sys.stdin.readline().strip()
        utt = {'utt':text, 'sessionId':"dummy"}
        print( aiml.reply(utt) )

