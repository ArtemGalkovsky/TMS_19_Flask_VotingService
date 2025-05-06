from databases.default_connection_class import DefaultConnection
from databases.creators.polls_tables_creator import Creator as PollsTablesCreator
from databases.exceptions import PollAlreadyExists
from config import POLLS_DATABASE_NAME

class PollsHandler(DefaultConnection):
    def __init__(self):
        super().__init__(POLLS_DATABASE_NAME)

        self.__polls_tables_creator = PollsTablesCreator(initial_tables_auto_creation=True)

    def add_poll(self, name: str, description: str) -> None:
        self._cursor.execute("""SELECT true
                                FROM polls
                                WHERE name = ?""", (name,))

        if self._cursor.fetchone():
            raise PollAlreadyExists(name)

        self._cursor.execute("""INSERT INTO polls (name, description) VALUES (?, ?)""", (name, description))
        self._connection.commit()

    def toggle_visibility(self, poll_name: str, visible: bool = True):
        self._cursor.execute("""UPDATE polls SET visible = ? WHERE name = ?""", (visible, poll_name))
        self._connection.commit()

    def update_poll(self, poll_name_to_update: str, new_description: str) -> None:
        self._cursor.execute("""UPDATE polls SET description = ? WHERE name = ?""", (new_description, poll_name_to_update))
        self._connection.commit()

    def get_all_polls(self):
        self._cursor.execute("""SELECT id, name, description FROM polls""")

        return self._cursor.fetchall()