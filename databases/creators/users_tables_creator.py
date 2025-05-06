from config import USERS_DATABASE_NAME
from databases.creators.default_creator import DefaultCreatorWithInitialTables

class Creator(DefaultCreatorWithInitialTables):
    def __init__(self, *, initial_tables_auto_creation: bool = False):
        super().__init__(USERS_DATABASE_NAME, initial_tables_auto_creation)

    def create_initial_tables(self, bypass_check_for_duplicate_creation: bool = False) -> bool:
        if self._already_created and not bypass_check_for_duplicate_creation:
            return False

        self._cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(50) NOT NULL,
            phone_number VARCHAR(15) NOT NULL,
            password VARCHAR(50) NOT NULL
        )''')
        self._connection.commit()

        self._already_created = True

        return True

