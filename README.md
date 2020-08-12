# 『Pythonでつくる対話システム』ソースコード＆データ配布とサポートページ

このリポジトリでは，オーム社から発売中の『[Pythonでつくる対話システム](https://www.ohmsha.co.jp/book/9784274224799/)』で使用するプログラムとデータ，およびサポートのためのページです．


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
書籍の誤植を発見された方は，[Issue]( https://github.com/dsbook/dsbook/issues/new)もしくはメール(dialoguesystemwithpythonあっとgmail.com)でご報告いただければ幸いです．
| 頁 | 行 | 誤 | 正 |
| --- | --- | --- | ---- |
| p.8 |図1.2の(出典)の2行目| Terry Winogra, "GUS, A Frame-Driven Dialog System," Artifical Intelligence, | Terry Winograd, "GUS, A Frame-Driven Dialog System," Artificial Intelligence, |
| p.61 |図2.7| date 天気 | type 天気 |
| p.224 | | 「キャラクタ性」のコラムが3章末と4章末に掲載されています．| [「対話システムとプライバシー」のコラム](/正誤表_Pythonでつくる対話システム（第1版第1刷200305）.pdf)が入ります． |

## よくある質問
**Q**：echo_system.pyなどTelegram上で対話システムを動かすプログラムを実行する際，「TelegramDeprecationWarning: Old Handler API is deprecated - see https://git.io/fxJuV for details」という警告が出ます．どうすればよいでしょうか？

**A**：Telegram APIのアップデートにより，そのようなメッセージが出るようになりました．そのままでも問題なく実行できますので，特別な対処は必要ありません．

## プログラムが動作しない場合の対処方法

本書籍で使用しているソフトウェア・APIのアップデート等に起因し，プログラムが本書籍通りに実行しても正しく動かない場合，[Issue]( https://github.com/dsbook/dsbook/issues/new) で報告をお願いします．

* learn_generative_model.ipynb
  * Google ColabのPyTorchのバージョンが上がったため正しく動作しなくなりました．そのため，最初にPyTorch 1.2.0をインストールするように修正しました．GitHub上のソースコードは修正済みです．
* PythonでMeCabを使用した際にRuntime Errorが出る
  * mecab-python3のバージョンにより正しく動作しない場合があります．バージョンを指定してインストールしてください (例: $pip install mecab-python3==0.996.5)
