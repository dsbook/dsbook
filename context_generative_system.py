from onmt.translate.translator import build_translator
import onmt.opts as opts
from onmt.utils.parse import ArgumentParser
import MeCab
from telegram_bot import TelegramBot


class ContextGenerativeSystem:
    def __init__(self):
        # コマンドラインで指定したオプションをもとにモデルを読み込む
        parser = ArgumentParser()
        opts.config_opts(parser)
        opts.translate_opts(parser)
        self.opt = parser.parse_args()
        ArgumentParser.validate_translate_opts(self.opt)
        self.translator = build_translator(self.opt, report_score=True)
        
        # 分かち書きのためにMeCabを使用
        self.mecab = MeCab.Tagger("-Owakati")
        self.mecab.parse("")
        
        # 前回の応答を保存しておく辞書
        self.prev_uttr_dict = {}


    def initial_message(self, input):
        message = 'こんにちは。対話を始めましょう。'
        self.prev_uttr_dict[input["sessionId"]] = message
        return {'utt': message, 'end':False}
        

    def reply(self, input):
        # 前回の応答と入力文をSEPを挟んで連結する
        context = self.prev_uttr_dict[input["sessionId"]] + " SEP " + input['utt']
        # 分かち書きにする
        src = [self.mecab.parse(context)[0:-2]]
        # ニューラルネットワークに分かち書きされた文脈を入力し，生成結果を得る
        _, predictions = self.translator.translate(
            src=src,
            tgt=None,
            src_dir=self.opt.src_dir,
            batch_size=self.opt.batch_size,
            attn_debug=False
        )
        # 生成結果も分かち書きされているので空白を削除
        generated_reply = predictions[0][0].replace(" ", "")
        # 次回の応答生成のために今回の応答を保存
        self.prev_uttr_dict[input["sessionId"]] = generated_reply
        return {"utt": generated_reply,  "end": False}


if __name__ == '__main__':
    system = ContextGenerativeSystem()
    bot = TelegramBot(system)
    bot.run()
    
