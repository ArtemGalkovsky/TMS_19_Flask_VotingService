from utils.singleton import Singleton
from databases.default_connection_class import DefaultConnection

class DefaultCreatorWithInitialTables(DefaultConnection, metaclass=Singleton):
    def __init__(self, table_name: str, initial_tables_auto_creation: bool = False):
        super().__init__(table_name)

        self._already_created: bool = False

        if initial_tables_auto_creation:
            self.create_initial_tables()

    def create_initial_tables(self, bypass_check_for_duplicate_creation: bool = False) -> bool:
        self._already_created = True

        return True