
# -*- coding: utf-8 -*-
"""
db.py — 数据访问层
封装 SQLite3 的增删查改，CLI 与 GUI 复用。

表结构：items
- id INTEGER PRIMARY KEY AUTOINCREMENT
- name TEXT NOT NULL
- description TEXT
- contact TEXT NOT NULL
- price REAL NOT NULL DEFAULT 0     # 0 表示赠送
- status TEXT NOT NULL DEFAULT 'available'  # available / done
- created_at TEXT ISO8601
"""
import sqlite3
from pathlib import Path
from datetime import datetime

SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  description TEXT,
  contact TEXT NOT NULL,
  price REAL NOT NULL DEFAULT 0,
  status TEXT NOT NULL DEFAULT 'available',
  created_at TEXT NOT NULL
);
"""

class ReviveDB:
    """SQLite 封装类，提供基础 CRUD 接口。"""
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        cur = self.conn.cursor()
        cur.executescript(SCHEMA)
        self.conn.commit()

    def add_item(self, name: str, description: str, contact: str, price: float = 0.0) -> int:
        now = datetime.now().isoformat(timespec='seconds')
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO items(name, description, contact, price, status, created_at) VALUES (?, ?, ?, ?, 'available', ?)",
            (name, description, contact, price, now)
        )
        self.conn.commit()
        return cur.lastrowid

    def delete_item(self, item_id: int) -> int:
        cur = self.conn.cursor()
        cur.execute("DELETE FROM items WHERE id = ?", (item_id,))
        self.conn.commit()
        return cur.rowcount

    def list_items(self, limit: int = 50, order_by: str = 'created_at', asc: bool = False):
        if order_by not in ('created_at', 'price', 'id', 'name'):
            order_by = 'created_at'
        direction = 'ASC' if asc else 'DESC'
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM items ORDER BY {order_by} {direction} LIMIT ?", (limit,))
        return cur.fetchall()

    def search_items(self, q: str, limit: int = 50):
        like = f"%{q}%"
        cur = self.conn.cursor()
        cur.execute(
            "SELECT * FROM items WHERE name LIKE ? OR description LIKE ? ORDER BY created_at DESC LIMIT ?",
            (like, like, limit)
        )
        return cur.fetchall()

    def export_csv(self, out_path: Path) -> int:
        import csv
        rows = self.list_items(limit=100000, order_by='created_at', asc=True)
        with open(out_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id','name','description','contact','price','status','created_at'])
            for r in rows:
                writer.writerow([r['id'], r['name'], r['description'] or '', r['contact'], r['price'], r['status'], r['created_at']])
        return len(rows)

    def close(self) -> None:
        self.conn.close()
