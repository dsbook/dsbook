# 『Pythonでつくる対話システム』ソースコード＆データ配布とサポートページ

このリポジトリでは，オーム社から発売中の『[Pythonでつくる対話システム](https://www.ohmsha.co.jp/book/9784274224799/)』で使用するプログラムとデータ，およびサポートのためのページです．

**(2022/04/28) 第1版第2刷の発行にあたり，第1刷からのアップデート情報を追加しました．第1刷をお持ちの方で，プログラムが動作しない場合はこちらをご覧ください** →  [アップデート情報](https://github.com/dsbook/dsbook/blob/master/eratta-taiwasystem_20220427.pdf)

**(2020/11/16) Telegramを使用せずに対話システムを実行可能にするプログラムを追加しました** →  [使用方法](https://github.com/dsbook/dsbook/blob/master/README_console_bot.md)

## プログラム

プログラムの解説は本書籍をご覧ください．


## データ

本リポジトリのデータを使用する場合は，以下を引用してください．
```
@misc{Pythonでつくる対話システム,
  title={Pythonでつくる対話システム},
  author={東中 竜一郎 and 稲葉 通将 and 水上 雅博},
  year={2020},
  publisher={オーム社}
}
```

## 正誤表
正誤表は[こちら](https://github.com/dsbook/dsbook/blob/master/eratta-taiwasystem_20220427.pdf)

正誤表には掲載されていない書籍の誤植を発見された方は，[Issue]( https://github.com/dsbook/dsbook/issues/new)もしくはメール(dialoguesystemwithpythonあっとgmail.com)でご報告いただければ幸いです．


## よくある質問
**Q**：echo_system.pyなどTelegram上で対話システムを動かすプログラムを実行する際，「TelegramDeprecationWarning: Old Handler API is deprecated - see https://git.io/fxJuV for details」という警告が出ます．どうすればよいでしょうか？

**A**：Telegram APIのアップデートにより，そのようなメッセージが出るようになりました．そのままでも問題なく実行できますので，特別な対処は必要ありません．

## プログラムが動作しない場合の対処方法

本書籍で使用しているソフトウェア・APIのアップデート等に起因し，プログラムが本書籍通りに実行しても正しく動かない場合，[Issue]( https://github.com/dsbook/dsbook/issues/new) で報告をお願いします．

### 現在までに判明している問題とその対処法

[アップデート情報](https://github.com/dsbook/dsbook/blob/master/eratta-taiwasystem_20220427.pdf)を参照してください．

### mecab-python3がインストールできない．
P.20のインストールコマンドを以下に変更してください．
```
$ pip install mecab-python3==0.996.1
```
