from config import POLLS_DATABASE_NAME
from databases.default_connection_class import DefaultConnection

class Creator(DefaultConnection):
    def __init__(self):
        super().__init__(POLLS_DATABASE_NAME)

    def create_table(self, poll_id: int) -> None:
        if not isinstance(poll_id, int):
            raise TypeError('poll_id must be of type int.')

        self._cursor.execute(f'''CREATE TABLE IF NOT EXISTS questions_{poll_id} (
            question_id INTEGER PRIMARY KEY NOT NULL,
            question_text TEXT
        )''')
        self._connection.commit()

