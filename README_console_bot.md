# console_bot.py

本書籍では，主にTelegram上で対話システムを実行しますが，console_bot.pyを用いることでコンソール上で実行することが可能になります．

## 使用方法

実行する対話システムのプログラム(echo_system.py, weather_system.pyなど)を以下のように修正してください．

* console_botのインポート
  * プログラムの先頭に以下を追加
    ```
    from console_bot import ConsoleBot
    ```
* TelegramBotを使用せず，ConsoleBotを使用するよう修正
  * ファイルの末尾近くにある以下を
    ```
    bot = TelegramBot(system)
    ```
  * 以下のように修正
    ```
    # bot = TelegramBot(system)
    bot = ConsoleBot(system)    
    ```
    
実行方法は修正前と同じです．
