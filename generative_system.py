from onmt.translate.translator import build_translator
import onmt.opts as opts
from onmt.utils.parse import ArgumentParser
import MeCab
from telegram_bot import TelegramBot


class GenerativeSystem:
    def __init__(self):
        # おまじない
        parser = ArgumentParser()
        opts.config_opts(parser)
        opts.translate_opts(parser)
        self.opt = parser.parse_args()
        ArgumentParser.validate_translate_opts(self.opt)
        self.translator = build_translator(self.opt, report_score=True)

        # 単語分割用にMeCabを使用
        self.mecab = MeCab.Tagger("-Owakati")
        self.mecab.parse("")

    def initial_message(self, input):
        return {'utt': 'こんにちは。対話を始めましょう。', 'end': False}

    def reply(self, input):
        # 単語を分割
        src = [self.mecab.parse(input["utt"])[0:-2]]
        # OpenNMTで応答を生成
        scores, predictions = self.translator.translate(
            src=src,
            tgt=None,
            src_dir=self.opt.src_dir,
            batch_size=self.opt.batch_size,
            attn_debug=False
        )
        # OpenNMTの出力も単語に分割されているので，半角スペースを削除
        utt = predictions[0][0].replace(" ", "")
        return {'utt': utt, "end": False}


if __name__ == '__main__':
    system = GenerativeSystem()
    bot = TelegramBot(system)
    bot.run()
    