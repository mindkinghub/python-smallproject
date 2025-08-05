import sqlite3
import csv
import sys
import os

DB_PATH = "../books.db"
EXPORT_CSV = "../books_links_template.csv"
IMPORT_CSV = "../books_links.csv"

def export_titles(only_missing=False):
    """导出书名模板，可选只导出缺少链接的"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if only_missing:
        cursor.execute("SELECT title, format FROM books WHERE link IS NULL OR link='' ORDER BY category, title")
    else:
        cursor.execute("SELECT title, format FROM books ORDER BY category, title")

    rows = cursor.fetchall()

    with open(EXPORT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "format", "link", "code"])  # 新增 format 字段
        for row in rows:
            writer.writerow([row["title"], row["format"], "link", "code"])  # 写入时也包含 format

    conn.close()
    mode = "缺链接书单" if only_missing else "全量书单"
    print(f"✅ 已导出 {len(rows)} 本书到 {EXPORT_CSV}（{mode}）")



def import_links():
    """从 CSV 批量导入链接和提取码"""
    if not os.path.exists(IMPORT_CSV):
        print(f"❌ 未找到 {IMPORT_CSV}，请先准备好 CSV 文件")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(IMPORT_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            title = row["title"].strip()
            link = row["link"].strip()
            code = row["code"].strip()

            cursor.execute(
                "UPDATE books SET link=?, code=? WHERE title=?",
                (link, code, title)
            )
            if cursor.rowcount > 0:
                count += 1
            else:
                print(f"⚠️ 数据库中未找到书名: {title}")

    conn.commit()
    conn.close()
    print(f"✅ 已更新 {count} 本书的下载链接和提取码")


def help_msg():
    print("""
使用方法：
    python book_links_tool.py export       # 导出所有书名模板到 books_links_template.csv
    python book_links_tool.py export-miss  # 仅导出缺少链接的书名模板
    python book_links_tool.py import       # 从 books_links.csv 批量导入链接和提取码
""")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        help_msg()
    elif sys.argv[1] == "export":
        export_titles()
    elif sys.argv[1] == "export-miss":
        export_titles(only_missing=True)
    elif sys.argv[1] == "import":
        import_links()
    else:
        help_msg()
