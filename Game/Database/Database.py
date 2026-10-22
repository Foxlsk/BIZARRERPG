from contextlib import contextmanager
import sqlite3
from Config import Config

class Database:
    DB_PATH = Config.DB_PATH
    
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

    @contextmanager
    def Use(db=None):
        """Reuses an open connection (to keep several operations in one transaction) or opens a new one."""
        if db is not None:
            yield db
        else:
            with Database.Connect() as con:
                yield con

    def Execute(query, params=(), db=None):
        with Database.Use(db) as con:
            cursor = con.execute(query, params)
            return cursor.rowcount

    def Insert(query, params=(), db=None):
        with Database.Use(db) as con:
            cursor = con.execute(query, params)
            return cursor.lastrowid

    def FetchOne(query, params=(), db=None):
        with Database.Use(db) as con:
            cursor = con.execute(query, params)
            return cursor.fetchone()

    def FetchAll(query, params=(), db=None):
        with Database.Use(db) as con:
            cursor = con.execute(query, params)
            return cursor.fetchall()

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

    def ColumnExists(table, column):
        with Database.Connect() as db:
            columns = db.execute(f'PRAGMA table_info("{table}")').fetchall()
            return any(row["name"] == column for row in columns)

    def IsEmpty(table):
        return Database.FetchOne(f'SELECT 1 FROM "{table}" LIMIT 1') is None

    def CreateTable(table, query):
        if not Database.TableExists(table):
            Database.Execute(query)
            print(f"[Database] {table} Table Created")
        else:
            print(f"[Database] {table} Loaded")
