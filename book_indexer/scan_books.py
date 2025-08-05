# scan_books.py
import os
import sqlite3
from pathlib import Path

BASE_DIR = r"D:\study\Course\Books"  # 你的书籍目录
DB_FILE = "books.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            category TEXT,
            format TEXT,
            size INTEGER,
            link TEXT,
            code TEXT
        )
    """)
    conn.commit()
    conn.close()

def scan_books():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("DELETE FROM books")  # 清空表

    for root, dirs, files in os.walk(BASE_DIR):
        category = Path(root).name
        for file in files:
            ext = file.split('.')[-1].upper()
            size = os.path.getsize(os.path.join(root, file))
            title = Path(file).stem

            c.execute("""
                INSERT INTO books (title, category, format, size, link, code)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (title, category, ext, size, "", ""))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    scan_books()
    print("✅ 数据库已更新")
