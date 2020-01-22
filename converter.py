import MeCab

class Converter:
    def __init__(self):
        self.tagger = MeCab.Tagger('-Owakati')

        self.convert_rules = [
            ('です 。', 'や ねん 。'),
            ('だよ 。', 'や で 。'),
            ('だ 。', 'や 。'),
            ('です か 。', 'やろ か 。'),
            ('かも 。', 'やろ なぁ 。'),
            ('だった 。', 'やった 。'),
            ]
    
    def convert(self, text):
        tokens = self.tagger.parse(text)
        for rule in self.convert_rules:
            tokens = tokens.replace(rule[0], rule[1])
        text = ''.join([ word for word in tokens.split()])
        return text

if __name__=='__main__':
    converter = Converter()
    text = '私はスキーが好きです。'
    print( converter.convert(text) )
