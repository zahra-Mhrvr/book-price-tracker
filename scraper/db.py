import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "books.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price REAL NOT NULL,
    rating INTEGER,
    availability TEXT,
    category TEXT,
    scraped_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(SCHEMA)
    return conn


def insert_books(books):
    conn = get_connection()
    with conn:
        conn.executemany(
            "INSERT INTO books (title, price, rating, availability, category) "
            "VALUES (:title, :price, :rating, :availability, :category)",
            books,
        )
    conn.close()


def clear_books():
    conn = get_connection()
    with conn:
        conn.execute("DELETE FROM books")
    conn.close()
