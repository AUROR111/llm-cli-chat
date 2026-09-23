import sqlite3
from src.bookkeeping.models import Transaction
from datetime import datetime

DB_FILE = "bookkeeping.db"

def init_db():
    #初始化数据库表
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            note TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_transaction(t: Transaction) -> int:
    #添加一条账单，返回id
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions(amount, category, note, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (t.amount, t.category, t.note, t.created_at.isoformat(), t.updated_at.isoformat()))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def get_all_transactions() -> list[Transaction]:
    #获取所有账单记录
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, amount, category, note,created_at, updated_at FROM transactions')
    rows = cursor.fetchall()
    conn.close()
    res = []
    for row in rows:
        t = Transaction(
            id=row[0],
            amount=row[1],
            category=row[2],
            note=row[3],
            created_at=datetime.fromisoformat(row[4]),
            updated_at=datetime.fromisoformat(row[5])
        )
        res.append(t)
    return res

def delete_transaction(tid:int):
    #根据id删除账单记录
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM transactions WHERE id = ?',(tid,))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        raise ValueError(f"记录ID{tid}不存在，无法删除。")
    conn.close()

def get_month_total(year_month:str):
    #按月统计，格式‘2026-09’
    try:
        year_str, month_str = year_month.split('-')
        year = int(year_str)
        month = int(month_str)
    except ValueError:
        raise ValueError("月份格式错误，应为YYYY-MM")
    
    if not (1 <= month <= 12):
        raise ValueError("月份应在1到12之间")
    #格式化，保证4位年份，2位月份
    year_month = f"{year:04d}-{month:02d}"

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT SUM(amount) FROM transactions
        WHERE strftime('%Y-%m', created_at) = ?
    ''',(year_month,))
    total = cursor.fetchone()[0] or 0.0
    conn.close()
    return total

def get_filter_transactions(category=None):
    all_records = get_all_transactions()
    if category:
        return [r for r in all_records if r.category == category]
    return all_records

def update_transaction(tid: int, new_amount=None, new_category=None, new_note=None):
    records = get_all_transactions()
    for r in records:
        if r.id == tid:
            if new_amount is not None:
                r.amount = new_amount
            if new_category is not None:
                r.category = new_category
            if new_note is not None:
                r.note = new_note
            r.updated_at = datetime.now()
            return r
    raise ValueError(f"ID {tid} 不存在")

