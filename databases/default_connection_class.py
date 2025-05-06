from sqlite3 import connect, Connection, Cursor

class DefaultConnection:
    def __init__(self, table_name: str):
        self._connection: Connection = connect(table_name)
        self._cursor: Cursor = self._connection.cursor()

    def destroy(self):
        if self._connection:
            self._connection.close()

    def __del__(self):
        self.destroy()