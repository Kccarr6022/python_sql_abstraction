import sqlite3
from typing import Dict, Optional


class SQLDriver:

    conn: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self, database_name: Optional[str] = None, in_memory: bool = False):
        try:
            self.conn: sqlite3.Connection = (
                sqlite3.connect(":memory:")
                if in_memory
                else sqlite3.connect(database_name or "database.db")
            )
            self.cursor: sqlite3.Cursor = self.conn.cursor()
        except sqlite3.Error as e:
            raise self.CreationError(e)

    def execute_raw(self, sql: str):
        """Executes raw SQL (ONLY FOR DDL).

        Args:
            sql (str): The SQL statement to execute.
        """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except sqlite3.Error as e:
            print("Problem executing sql:", e)
            self.conn.rollback()

    def execute_statement(self, sql: str, params: Dict):
        """Executes a SQL statement.

        Args:
            sql (str): The SQL statement to execute.
            params (Dict): The parameters to use in the SQL statement.
        """
        try:
            self.cursor.execute(sql, params)
            self.conn.commit()
        except sqlite3.Error as e:
            print("Problem executing sql:", e)
            self.conn.rollback()

    def __del__(self):
        self.conn.close()

    class CreationError(Exception):
        pass
