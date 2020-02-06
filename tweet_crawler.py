import tweepy
import random
import re


while True:
    # ここに先程取得したAPIキーとトークンを入力
    api_key = ""
    api_secret_key = ""
    access_token = ""
    access_token_secret = ""

    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True)

    # botのツイートを除外するため，一般的なクライアント名を列挙
    sources = ["TweetDeck", "Twitter Web Client", "Twitter for iPhone",
               "Twitter for iPad", "Twitter for Android", "Twitter for Android Tablets",
               "ついっぷる", "Janetter", "twicca", "Keitai Web", "Twitter for Mac"]
    

    # ひらがな一文字で検索し，スクリーンネームを取得
    words = list("あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん")
    
    screen_names = set()
    for s in api.search(q=random.choice(words), lang='ja', result_type='recent', count=100, tweet_mode='extended'):
        if s.source in sources:
            screen_names.add(s.author.screen_name)

    # ステータスidからステータスを得るためのdict
    id2status = {}

    # スクリーンネームからタイムラインを取得してツイートを保存．
    # さらにリプライツイートであれば，リプライ先のスクリーンネームも取得
    in_reply_to_screen_names = set()
    for name in screen_names:
        try:
            for s in api.user_timeline(name, tweet_mode='extended', count=200):
                # リンクもしくはハッシュタグを含むツイートは除外する
                if "http" not in s.full_text and "#" not in s.full_text:
                    id2status[s.id] = s
                    if s.in_reply_to_screen_name is not None:
                        if s.in_reply_to_screen_name not in screen_names:
                            in_reply_to_screen_names.add(s.in_reply_to_screen_name)
        except Exception as e:
            continue

    # リプライ先のスクリーンネームからタイムラインを取得してツイートを保存
    for name in in_reply_to_screen_names:
        try:
            for s in api.user_timeline(name, tweet_mode='extended', count=200):
                if "http" not in s.full_text and "#" not in s.full_text:
                    id2status[s.id] = s
        except Exception as e:
            continue

    # 保存したツイートのリプライ先のツイートが保存されていれば，id2replyidのキーを元ツイートのid，値をリプライ先ツイートのidとする
    id2replyid = {}
    for _, s in id2status.items():
        if s.in_reply_to_status_id in id2status:
            id2replyid[s.in_reply_to_status_id] = s.id


    # id2replyidのkey valueからstatusを取得し，ツイートペアをタブ区切りで保存
    f = open("tweet_pairs.txt", "a")
    for id, rid in id2replyid.items():
        # 改行は半角スペースに置換
        tweet1 = id2status[id].full_text.replace("\n", " ")
        # スクリーンネームを正規表現を用いて削除
        tweet1 = re.sub(r"@[0-9a-zA-Z_]{1,15} +", "", tweet1)

        tweet2 = id2status[rid].full_text.replace("\n", " ")
        tweet2 = re.sub(r"@[0-9a-zA-Z_]{1,15} +", "", tweet2)

        f.write(tweet1+ "\t" + tweet2 + "\n")
    f.close()
    print("Write " + str(len(id2replyid)) + " pairs.")


    # ツイート3組をタブ区切りで保存
    # f = open("tweet_triples.txt", "a")
    # for id, rid in id2replyid.items():
    #     if rid in id2replyid:
    #         tweet1 = id2status[id].full_text.replace("\n", " ")
    #         tweet1 = re.sub(r"@[0-9a-zA-Z_]{1,15} +", "", tweet1)

    #         tweet2 = id2status[rid].full_text.replace("\n", " ")
    #         tweet2 = re.sub(r"@[0-9a-zA-Z_]{1,15} +", "", tweet2)

    #         tweet3 =  id2status[id2replyid[rid]].full_text.replace("\n", " ")
    #         tweet3 = re.sub(r"@[0-9a-zA-Z_]{1,15} +", "", tweet3)
    #         f.write(tweet1 + " SEP " + tweet2 + "\t" + tweet3 + "\n")
    # f.close()


