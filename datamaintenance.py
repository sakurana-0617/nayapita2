import sqlite3
import random
from flask import Flask, render_template, request, redirect, session
from flask.wrappers import Request
import json
import requests

app = Flask(__name__)
app.secret_key = "SUNABACO"


@app.route("/")
def index():
    return redirect("/tasklist")


@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect('scm.db')
    c = conn.cursor()
    c.execute("delete from T_book where book_ID= ? ", (str(id),))
    conn.commit()
    conn.close()

    # print(user_info)
    return redirect("/tasklist")


@app.route("/edit/<int:id>", methods=["POST"])
def edit_post(id):
    py_comment = request.form.get("comment")
    py_woryy_ID = request.form.get("worry_ID")
    conn = sqlite3.connect('scm.db')
    c = conn.cursor()
    c.execute("UPDATE T_book SET comment = ? , worry_ID = ? WHERE book_ID = ?",
              (py_comment, py_woryy_ID, str(id)))
    conn.commit()
    conn.close()
    return redirect("/tasklist")


@app.route("/edit/<int:id>")
def edit(id):

    conn = sqlite3.connect('scm.db')
    c = conn.cursor()
    c.execute(
        "select comment,worry_ID from T_book where book_ID = ?", (id,))
    comment = c.fetchone()

    if comment is None:
        c.close()
        conn.close()
        return redirect("/tasklist")
    else:
        return_comment = comment[0]
        worry_ID = comment[1]
    c.close()
    conn.close()

    item = {"book_ID": id, "comment": return_comment, "worry_ID": worry_ID}
    return render_template("edit.html", item=item)


@app.route("/tasklist")
def tasklist():
    conn = sqlite3.connect('scm.db')
    c = conn.cursor()
    c.execute("select * from T_book  order by worry_ID ASC")
    task_all = c.fetchall()

    task_list = []

    for row in task_all:
        img_URL = "https://www.hanmoto.com/bd/img/" + row[2] + ".jpg"
        # open db に接続
        endpoint = "https://api.openbd.jp/v1/get"
        headers = {

        }
        params = {
            "isbn": row[2]
        }
        result = requests.get(endpoint, headers=headers, params=params)
        res = result.json()
        err_msg = ""
        title = ""
        publisher = ""
        author = ""
        if res[0] is not None:

            title = res[0]["onix"]["DescriptiveDetail"]["TitleDetail"]["TitleElement"]["TitleText"]["content"]
            publisher = res[0]["onix"]["PublishingDetail"]["Imprint"]["ImprintName"]
            author = ""
            for book_author in res[0]["onix"]["DescriptiveDetail"]["Contributor"]:  # 著者が複数人の場合
                author = book_author["PersonName"]["content"]

        else:
            err_msg = "本情報が取ってこれない"
        c = conn.cursor()
        c.execute("select worry from T_worry where worry_ID = ? ", (row[6],))
        nayami = c.fetchone()[0]

        task_list.append({"book_ID": row[0], "created_at": row[1], "ISBN": row[2],
                          "store": row[3], "staff": row[4], "comment": row[5], "worry_ID": row[6], "img_URL": img_URL, "title": title, "publisher": publisher, "author": author, "nayami": nayami, "err_msg": err_msg})
    c.close()
    conn.close()

    # print(user_info)
    return render_template("tasklist.html", task_list=task_list)


@app.errorhandler(404)
def notfound(code):
    return "404だよ"


if __name__ == "__main__":
    app.run(debug=True)
