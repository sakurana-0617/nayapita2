import random
from datetime import datetime
import os
# splite3をimportする
import sqlite3
# twitter用
import urllib.parse
# flaskをimportしてflaskを使えるようにする
from flask import Flask, render_template, request, redirect, session
# jsonをimport
import json
# requests(PythonのHTTP通信ライブラリ)をimport
import requests
# QRコード作成
import qrcode
# QRコード表示
from PIL import Image
# QRコードHTML表示
from io import BytesIO
import base64
# appにFlaskを定義して使えるようにしています。Flask クラスのインスタンスを作って、 app という変数に代入しています。
app = Flask(__name__)

# Flask では標準で Flask.secret_key を設定すると、sessionを使うことができます。この時、Flask では session の内容を署名付きで Cookie に保存します。
app.secret_key = 'sunabakoza'


@app.route('/')
def index():

    comment = ("熱いものを食べるのは、人間だけなんだって！", "実はアイスやガムには賞味期限がないんだって！",
               "卵に印刷されているのは、生卵として食べられる期間なんだって！", "立ちくらみの正式名称は眼前暗黒感っていうんだって！", "１円玉１枚を作るための材料費は２円かかるんだって！")
    comment += ("「かぼちゃ」は英語でスクワッシュ（squash）。パンプキン（pumpkin）だと思っている人も多いけど、パンプキンというのはハロウィンでよく見かけるオレンジ色のかぼちゃだけを意味するんだって！",
                "飛行機の機長と副操縦士は、２人同時に食中毒にかかるリスクを避けるために、フライト前に同じ食事を食べないんだって！")
    comment += ("ブラジルの首都はサンパウロでもリオデジャネイロでもなく「ブラジリア」なんだって！", "日本の歯医者の数はコンビニの数より多いんだって！",
                "南極ではどんなに寒くても人が風邪をひくことはないんだって！これは、あまりの寒さのためにウィルスが存在していないためだそう。")
    comment += ("ケンタッキーフライドチキン（ＫＦＣ）の、味付けのレシピを知っている人物は世界中にたった２人しかいないんだって！",
                "宝くじで１等が当選する確率よりも、隕石が自分に落ちてくる確率の方が高いんだって！")
    comment += ("扇風機は長年使用し続けると突然発火する恐れがあるから、定期的に買い替えなくちゃならないんだって！。（大体６年～１０年）", "海上自衛隊の金曜日のメニューは必ずカレーと決まっている。これは常に海の上で生活していて曜日の感覚を失わないようにするためなんだって！",
                "キュウリは世界で一番栄養がない野菜としてギネス認定されているんだって！", "サハラ砂漠の「サハラ」は砂漠という意味。訳すと砂漠砂漠になるんだって！")
    fun_comment = random.choice(comment)

    return render_template('top.html', fun_comment=fun_comment)


@app.route('/main')
def main():
    conn = sqlite3.connect('scm.db')
    c = conn.cursor()
    c.execute("select worry_ID , worry from T_worry")
    nayami = c.fetchall()
    c.close()
    conn.close()

    # nayami_listをランダムに並び替えて8つ選ぶ

    nayami_rand = random.sample(nayami, 8)
    nayami_list = []
    for row in nayami_rand:
        nayami_list.append({"worry_ID": row[0], "worry": row[1]})

    return render_template('main.html', nayami=nayami_list)


@app.route('/test', methods=["POST"])
def test():
    worry_ID = request.form.get("worry_ID")
    # print(worry_ID)
    conn = sqlite3.connect('scm.db')
    c = conn.cursor()
    c.execute("select worry from T_worry where worry_ID = ?", (worry_ID,))
    # print(worry_ID)
    onayami = c.fetchone()[0]
    c.execute(
        "select book_ID , ISBN ,comment,store,staff from T_book where worry_ID = ?", (worry_ID,))
    book_list = []
    for row in c.fetchall():
        # print(row)
        book_list.append(
            {"book_Id": row[0], "ISBN": row[1], "comment": row[2], "store": row[3], "staff": row[4]})
    c.close()
    conn.close()

    if not len(book_list) == 0:

        random_ID = random.randint(0, len(book_list)-1)
        book_isbn = book_list[random_ID]['ISBN']
        # worry_Id,ISBNを/resultに渡す---ここまでにbook_isbn、worry_IDを取ってくる
        # print(book_isbn)
        # print(worry_ID)
        return redirect('/result' + "?i=" + book_isbn + "&w=" + worry_ID)
    else:
        pass


@app.route('/result', methods=["GET"])
def result():
    # /testから送られてきたbook_isbn,worry_IDを取り出す
    req = request.args
    book_isbn = req.get("i")
    worry_ID = req.get("w")
    # print(book_isbn)
    # print(worry_ID)

    conn = sqlite3.connect('scm.db')
    c = conn.cursor()
    c.execute("select worry from T_worry where worry_ID = ?", (worry_ID,))
    onayami = c.fetchone()[0]
    c.execute(
        "select book_ID,ISBN,store,staff,comment from T_book where ISBN = ?", (book_isbn,))
    book_list = c.fetchall()
    # c.execute()
    # "select book_ID , ISBN ,comment,store,staff from T_book where worry_ID = ?", (worry_ID,))
    # book_list = []
    # for row in c.fetchall():
    #     # print(row)
    # book_list.append(
    # {"book_Id": row[0], "ISBN": row[1], "comment": row[2], "store": row[3], "staff": row[4]})
    c.close()
    conn.close()
    # if not len(book_list) == 0:
    #     random_ID = random.randint(0, len(book_list)-1)
    #     book_isbn = book_list[random_ID]['ISBN']
    #     # book_isbn = '9784750352589'
    #     # print(book_isbn)
    #     # ここbook_isbnでISBNから書誌情報を取ってくる
    img_URL = "https://www.hanmoto.com/bd/img/" +\
        book_isbn + ".jpg"

    buy_URL = "https://www.honyaclub.com/shop/affiliate/itemlist.aspx?isb=871150&isbn=" + book_isbn
    #HerokuにはこのURLを変えること#
    book_URL = "https://nayapita2.herokuapp.com/" + 'result' + \
        "?i=" + book_isbn + "&w=" + worry_ID
    # open db に接続
    endpoint = "https://api.openbd.jp/v1/get"
    headers = {

    }
    params = {
        "isbn": book_isbn
    }
    result = requests.get(endpoint, headers=headers, params=params)
    res = result.json()
    # print(res)
    if res[0] is not None:

        title = res[0]["onix"]["DescriptiveDetail"]["TitleDetail"]["TitleElement"]["TitleText"]["content"]
        publisher = res[0]["onix"]["PublishingDetail"]["Imprint"]["ImprintName"]
        author = ""
        for book_author in res[0]["onix"]["DescriptiveDetail"]["Contributor"]:  # 著者が複数人の場合
            author = book_author["PersonName"]["content"]

        # print(book_list[0][4])
        comment = book_list[0][4]
        store = book_list[0][2]
        staff = book_list[0][3]
        book_list[0][1]
        tweet_comment = "「"+onayami+"」お悩みにはこの本がおススメ！「" + \
            title+"」"+comment+"　　powered by なやみぴたっと"
        tweeturl = post_tweet(tweet_comment, book_URL)

        # qr = qrcode.QRCode(box_size=2)        # box_size= xx の数が多いと黒と白の四角(セル)が大きくなる
        # qr.add_data('/result?i=?&w=?') # QRコードにしたい文字列
        # # qr.add_data('result?i=?&w=?') # 続きのQRコードにしたい文字列
        # qr.make()                # QRコードを生成する
        # img = qr.make_image()  # 生成したイメージを取り出す
        # img.show()   #イメージを出力
        # # image.save('')

        return render_template('result.html', onayami=onayami, img_URL=img_URL, title=title, publisher=publisher, author=author, comment=comment, tweeturl=tweeturl, store=store, staff=staff,buy_URL=buy_URL)
    else:
        return render_template('result_zero.html', onayami=onayami)

# else:
#     return render_template('result_zero.html', onayami=onayami)


# ----------------------------------------------
# tweet自動生成
TWITTER_BASE = "https://twitter.com/"
# tweet投稿


def post_tweet(text, url):

    tweet_text = text
    tweet_text = urllib.parse.quote(tweet_text, safe='')

    tweet_url = url
    tweet_url = urllib.parse.quote(tweet_url, safe='')

    target_url = TWITTER_BASE + "intent/tweet?text=" + \
        tweet_text + "&url=" + tweet_url

    # 投稿画面へ遷移
    return target_url


@app.route('/register', methods=["POST"])
def register():
    #  登録ページを表示させる
    # 登録ページで登録ボタンを押した時に走る処理
    name = request.form.get("name")
    team = request.form.get("team")
    osusume_book = request.form.get("osusume_book")
    if name+team+osusume_book != "":
        time = datetime.now()
        conn = sqlite3.connect('scm.db')
        c = conn.cursor()
        c.execute("insert into T_recommend values(null,?,?,?,?)",
                  (time, osusume_book, team, name))
        conn.commit()
        conn.close()

    comment = ("熱いものを食べるのは、人間だけなんだって！", "実はアイスやガムには賞味期限がないんだって！",
               "卵に印刷されているのは、生卵として食べられる期間なんだって！", "立ちくらみの正式名称は眼前暗黒感っていうんだって！", "１円玉１枚を作るための材料費は２円かかるんだって！")
    comment += ("「かぼちゃ」は英語でスクワッシュ（squash）。パンプキン（pumpkin）だと思っている人も多いけど、パンプキンというのはハロウィンでよく見かけるオレンジ色のかぼちゃだけを意味するんだって！",
                "飛行機の機長と副操縦士は、２人同時に食中毒にかかるリスクを避けるために、フライト前に同じ食事を食べないんだって！")
    comment += ("ブラジルの首都はサンパウロでもリオデジャネイロでもなく「ブラジリア」なんだって！", "日本の歯医者の数はコンビニの数より多いんだって！",
                "南極ではどんなに寒くても人が風邪をひくことはないんだって！これは、あまりの寒さのためにウィルスが存在していないためだそう。")
    comment += ("ケンタッキーフライドチキン（ＫＦＣ）の、味付けのレシピを知っている人物は世界中にたった２人しかいないんだって！",
                "宝くじで１等が当選する確率よりも、隕石が自分に落ちてくる確率の方が高いんだって！")
    comment += ("扇風機は長年使用し続けると突然発火する恐れがあるから、定期的に買い替えなくちゃならないんだって！。（大体６年～１０年）", "海上自衛隊の金曜日のメニューは必ずカレーと決まっている。これは常に海の上で生活していて曜日の感覚を失わないようにするためんだって！",
                "キュウリは世界で一番栄養がない野菜としてギネス認定されているんだって！", "サハラ砂漠の「サハラ」は砂漠という意味。訳すと砂漠砂漠になるんだって！")
    fun_comment = random.choice(comment)
    return render_template('thankyou.html', fun_comment=fun_comment)


@app.errorhandler(403)
def mistake403(code):
    return 'There is a mistake in your url!'


@app.errorhandler(404)
def notfound(code):
    return "404だよ！！見つからないよ！！！"


#####ここは必要よ#####


if __name__ == "__main__":
    # Flask が持っている開発用サーバーを、実行します。
    app.run(debug=False)
