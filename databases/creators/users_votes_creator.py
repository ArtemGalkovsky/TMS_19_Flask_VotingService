from config import USERS_VOTES_DATABASE_NAME
from databases.default_connection_class import DefaultConnection

class Creator(DefaultConnection):
    def __init__(self):
        super().__init__(USERS_VOTES_DATABASE_NAME)

    def create_table(self, poll_id: int) -> None:
        self._cursor.execute(f'''CREATE TABLE users_votes_{poll_id} (
            username VARCHAR(50) REFERENCES users(username) NOT NULL,
            votes JSON NOT NULL DEFAULT '[]'
        )''')
        self._connection.commit()

