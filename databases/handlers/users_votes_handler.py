from databases.default_connection_class import DefaultConnection
from databases.creators.users_votes_creator import Creator as UsersVotesTablesCreator
from databases.exceptions import UserAlreadyVoted, PollNotFound
from config import USERS_VOTES_DATABASE_NAME
from sqlite3 import OperationalError

class UsersVotesHandler(DefaultConnection):
    def __init__(self):
        super().__init__(USERS_VOTES_DATABASE_NAME)

        self.__polls_tables_creator = UsersVotesTablesCreator()

    def is_poll_table_exists(self, poll_id: int) -> bool:
        try:
            self._cursor.execute(f"""SELECT true FROM users_votes_{poll_id}""", ())
            return True
        except OperationalError:
            return False

    def is_user_votes(self, poll_id: int, username: str) -> bool:
        if not self.is_poll_table_exists(poll_id):
            raise PollNotFound(poll_id)

        self._cursor.execute(f"""SELECT true
                                FROM users_votes_{poll_id}
                                WHERE username = ?""", (username,))

        if self._cursor.fetchone():
            return True

        return False

    def add_vote(self, poll_id: int, username: str, votes: dict) -> None:
        if self.is_user_votes(poll_id, username):
            raise UserAlreadyVoted(username)

        self._cursor.execute(f"""INSERT INTO users_votes_{poll_id} (username, votes) VALUES (?, ?)""",
                             (username, votes))
        self._connection.commit()

    def update_user_votes(self, poll_id: int, username_to_update: str, votes: dict) -> None:
        if not self.is_user_votes(poll_id, username_to_update):
            self.add_vote(poll_id, username_to_update, votes)
            return

        self._cursor.execute(f"""UPDATE users_votes_{poll_id} SET votes = ? WHERE username = ?""",
                             (votes, username_to_update))
        self._connection.commit()


if __name__ == '__main__':
    handler = UsersVotesHandler()

    handler.update_user_votes(1, "Artem", {"hello": "world"})
    print(handler.is_user_votes(1, "Artem"))