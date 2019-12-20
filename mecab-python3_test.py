import MeCab

mecab = MeCab.Tagger()

# python3-mecabのバグ回避のため，空文字をparse
mecab.parse('')

# 標準入力からテキストを受け取る
text = input(">")

node = mecab.parseToNode(text)
while node:
    print(node.surface, node.feature)
    node = node.next
