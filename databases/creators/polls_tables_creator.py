from config import POLLS_DATABASE_NAME
from databases.creators.default_creator import DefaultCreatorWithInitialTables

class Creator(DefaultCreatorWithInitialTables):
    def __init__(self, *, initial_tables_auto_creation: bool = False):
        super().__init__(POLLS_DATABASE_NAME, initial_tables_auto_creation)

    def create_initial_tables(self, bypass_check_for_duplicate_creation: bool = False) -> bool:
        if self._already_created and not bypass_check_for_duplicate_creation:
            return False

        self._cursor.execute('''CREATE TABLE IF NOT EXISTS polls(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            data JSON NOT NULL DEFAULT '[]',
            votes_table_id INTEGER NOT NULL,
            visible BOOLEAN NOT NULL
                                )''')
        self._connection.commit()

        self._already_created = True

        return True

