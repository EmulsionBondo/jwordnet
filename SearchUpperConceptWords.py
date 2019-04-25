import sqlite3
import sys
conn = sqlite3.connect("wnjpn.db")

# 上位-下位の関係にある概念の抽出
hierarchy_dict = {}  # key:上位語(String), value:下位語(List of String)
n_term_set = set()  # 下位語に含まれる単語集合

class node:
    def __init__(self, name, children=None):
        self.name = name  # String
        self.children = children  # List of Class node

    # 結果表示用
    def display(self, indent = 0):
        if self.children != None:
            print(' '*indent + self.name)
            for c in self.children:
                c.display(indent+1)
        else:
            print(' '*indent + self.name)

# 特定の単語を入力とした時に、上位語を検索する関数
def SearchUpperConceptWords(word, hierarchy_dict):

    # 問い合わせしたい単語がWordnetに存在するか確認する
    cur = conn.execute("select wordid from word where lemma='%s'" % word)
    word_id = 99999999  #temp
    for row in cur:
        word_id = row[0]
    # Wordnetに存在する語であるかの判定
    if word_id==99999999:
        print("「%s」は、Wordnetに存在しない単語です。" % word)
        return
    else:
        print("【「%s」の上位概念を出力します】\n" % word)

    # 入力された単語を含む概念を検索する
    cur = conn.execute("select synset from sense where wordid='%s'" % word_id)
    synsets = []
    for row in cur:
        synsets.append(row[0])

    for synset in synsets:
        #上位語を取得する対象のsynsetを表示
        print('------------------%s---------------------'% synset_name_dict[synset])
        #現在のsynsetの上位語をすべて取得するため，tmp_synsetに代入
        tmp_synset=synset
        #synsetの上位語を最上位まで列挙する
        while(tmp_synset in hierarchy_dict.values()):
            #エラーが発生=最上位語を取得したら終了
            try:
                print(synset_name_dict[hierarchy_dict[tmp_synset]])
                tmp_synset = hierarchy_dict[tmp_synset]
            except:
                break

# 下位-上位の関係にある概念の抽出
cur = conn.execute("select synset1,synset2 from synlink where link='hypo'")

hierarchy_dict = {}  # key:下位語(String), value:上位語(String)

for row in cur:
    b_term = row[0]
    n_term = row[1]

    if n_term not in hierarchy_dict:
        hierarchy_dict[n_term] = b_term

# synset(概念)のIDから、概念の名称に変換する辞書の作成
synset_name_dict = {}  # key:synsetのID, value:synsetの名称
cur = conn.execute("select synset,name from synset")
for row in cur:
    synset_name_dict[row[0]] = row[1]

SearchUpperConceptWords("猫", hierarchy_dict)
