from config import POLLS_DATABASE_NAME
from databases.creators.default_creator import DefaultCreatorWithInitialTables

class Creator(DefaultCreatorWithInitialTables):
    def __init__(self, *, initial_tables_auto_creation: bool = False):
        super().__init__(POLLS_DATABASE_NAME, initial_tables_auto_creation)

    def create_initial_tables(self) -> bool:
        self._cursor.execute('''CREATE TABLE IF NOT EXISTS polls(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            multiple_votes_enabled BOOLEAN NOT NULL DEFAULT FALSE,
            visible BOOLEAN NOT NULL
                                )''')
        self._connection.commit()

        return True

