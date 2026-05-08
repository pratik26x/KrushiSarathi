"""
Create farmers_db schema and load demo users + appointments.
Uses MySQL: host localhost, user root, password root (same as app.py).

Run from project root:
  python init_database.py
"""
from __future__ import annotations

import os
import sys

import mysql.connector
from mysql.connector import errors as mysql_errors

ROOT = os.path.dirname(os.path.abspath(__file__))
SETUP_SQL = os.path.join(ROOT, "setup_mysql.sql")
SEED_SQL = os.path.join(ROOT, "seed_mysql.sql")

CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
}


def _split_statements(sql: str):
    """Split on ';' and drop comment-only / empty chunks (sufficient for our SQL files)."""
    chunks = []
    for raw in sql.split(";"):
        lines = []
        for line in raw.splitlines():
            s = line.strip()
            if s.startswith("--"):
                continue
            lines.append(line)
        stmt = "\n".join(lines).strip()
        if stmt:
            chunks.append(stmt)
    return chunks


def _run_script(cursor, path: str) -> None:
    with open(path, encoding="utf-8") as f:
        sql = f.read()
    for stmt in _split_statements(sql):
        cursor.execute(stmt)
        if cursor.description:
            cursor.fetchall()


def main() -> int:
    print("Connecting to MySQL as root...")
    try:
        conn = mysql.connector.connect(**CONFIG)
    except mysql_errors.Error as e:
        print("Failed to connect:", e)
        print("Ensure MySQL Server is running and root password is 'root'.")
        return 1

    cursor = conn.cursor()
    try:
        print("Applying", SETUP_SQL)
        _run_script(cursor, SETUP_SQL)
        conn.commit()
        # Ensure password column fits werkzeug scrypt hashes on older DBs
        try:
            cursor.execute("USE farmers_db")
            cursor.execute(
                "ALTER TABLE users MODIFY COLUMN password VARCHAR(512) NOT NULL"
            )
            conn.commit()
        except mysql_errors.Error:
            conn.rollback()

        print("Applying", SEED_SQL)
        _run_script(cursor, SEED_SQL)
        conn.commit()
    except mysql_errors.Error as e:
        print("SQL error:", e)
        conn.rollback()
        return 1
    finally:
        cursor.close()
        conn.close()

    print("Done. Demo logins:")
    print("  ravi@krushisarathi.local   /  farmer123")
    print("  priya@krushisarathi.local  /  farmer123")
    print("  amit@example.in            /  demo2026")
    return 0


if __name__ == "__main__":
    sys.exit(main())
