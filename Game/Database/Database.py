from contextlib import contextmanager
import os
import sqlite3

class Database:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "Database.db")

    @contextmanager
    def Connect():
        con = sqlite3.connect(Database.DB_PATH)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys = ON")

        try:
            with con:
                yield con
        finally:
            con.close()

    def Execute(query, params=()):
        with Database.Connect() as db:
            cursor = db.execute(query, params)
            return cursor.rowcount

    def FetchOne(query, params=()):
            with Database.Connect() as db:
                cursor = db.execute(query, params)
                return cursor.fetchone()

    def DropTable(table):
        with Database.Connect() as db:
            db.execute(f'DROP TABLE IF EXISTS "{table}"')

    def ClearTable(table):
        with Database.Connect() as db:
            db.execute(f'DELETE FROM "{table}"')

    def TableExists(table):
        result = Database.FetchOne(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'table' AND name = ?",
            (table,)
        )
        return result is not None