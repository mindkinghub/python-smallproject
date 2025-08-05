# app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("books.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db()
    categories = conn.execute("SELECT DISTINCT category FROM books").fetchall()
    conn.close()
    return render_template("index.html", categories=categories)

@app.route("/category/<name>")
def category(name):
    conn = get_db()
    books = conn.execute("SELECT * FROM books WHERE category=?", (name,)).fetchall()
    conn.close()
    return render_template("category.html", category=name, books=books)

@app.route("/search")
def search():
    q = request.args.get("q", "")
    conn = get_db()
    books = conn.execute("SELECT * FROM books WHERE title LIKE ?", (f"%{q}%",)).fetchall()
    conn.close()
    return render_template("search.html", q=q, books=books)

@app.route("/edit/<int:book_id>", methods=["GET", "POST"])
def edit(book_id):
    conn = get_db()
    if request.method == "POST":
        link = request.form["link"]
        code = request.form["code"]
        conn.execute("UPDATE books SET link=?, code=? WHERE id=?", (link, code, book_id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    else:
        book = conn.execute("SELECT * FROM books WHERE id=?", (book_id,)).fetchone()
        conn.close()
        return render_template("edit.html", book=book)

if __name__ == "__main__":
    app.run(debug=True)
