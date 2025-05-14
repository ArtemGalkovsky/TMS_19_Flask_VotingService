from utils.singleton import Singleton
from databases.default_connection_class import DefaultConnection

class DefaultCreatorWithInitialTables(DefaultConnection, metaclass=Singleton):
    def __init__(self, table_name: str, initial_tables_auto_creation: bool = False):
        super().__init__(table_name)

        if initial_tables_auto_creation:
            self.create_initial_tables()

    def create_initial_tables(self) -> bool:
        return True