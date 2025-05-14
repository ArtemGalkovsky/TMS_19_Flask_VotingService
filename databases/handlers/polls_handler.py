from databases.default_connection_class import DefaultConnection
from databases.creators.polls_tables_creator import Creator as PollsTablesCreator
from databases.exceptions import PollAlreadyExists, PollNotFound
from config import POLLS_DATABASE_NAME

class PollsHandler(DefaultConnection):
    def __init__(self):
        super().__init__(POLLS_DATABASE_NAME)

        self.__polls_tables_creator = PollsTablesCreator(initial_tables_auto_creation=True)

    def is_poll_exists(self, name: str) -> bool:
        self._cursor.execute("""SELECT true
                                FROM polls
                                WHERE name = ?""", (name,))

        if self._cursor.fetchone():
            return True

        return False

    def add_poll(self, name: str, description: str, multiple_votes_enabled: bool = False) -> None:
        if self.is_poll_exists(name):
            raise PollAlreadyExists(name)

        self._cursor.execute("""INSERT INTO polls (name, description, multiple_votes_enabled, visible) 
                                VALUES (?, ?, ?, TRUE)""",
                             (name, description, multiple_votes_enabled))
        self._connection.commit()

    def toggle_visibility(self, poll_name: str, visible: bool = True):
        if not self.is_poll_exists(poll_name):
            raise PollNotFound(poll_name)

        self._cursor.execute("""UPDATE polls SET visible = ? WHERE name = ?""", (visible, poll_name))
        self._connection.commit()

    def update_poll(self, poll_name_to_update: str, new_description: str, multiple_votes_enabled: bool = False) -> None:
        if not self.is_poll_exists(poll_name_to_update):
            raise PollNotFound(poll_name_to_update)

        self._cursor.execute("""UPDATE polls SET description = ?, multiple_votes_enabled = ?
                                WHERE name = ?""",
                             (new_description, multiple_votes_enabled, poll_name_to_update))
        self._connection.commit()

    def get_all_polls(self):
        self._cursor.execute("""SELECT id, name, description FROM polls""")

        return self._cursor.fetchall()

    def get_last_poll_id(self):
        self._cursor.execute("""SELECT id FROM polls ORDER BY id DESC LIMIT 1""")
        last_id = self._cursor.fetchone()

        return 0 if not last_id else last_id[0]

    def get_poll_data(self, poll_id: int) -> dict:
        self._cursor.execute("""SELECT name, description, multiple_votes_enabled 
                                FROM polls WHERE id = ?""",
                             (poll_id,))

        return self._cursor.fetchone()