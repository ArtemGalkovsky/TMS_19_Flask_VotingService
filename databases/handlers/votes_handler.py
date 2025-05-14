from databases.default_connection_class import DefaultConnection
from databases.creators.questions_tables_creator import Creator as QuestionsTablesCreator
from databases.exceptions import IPAlreadyVoted, PollNotFound
from config import POLLS_DATABASE_NAME
from sqlite3 import OperationalError

class VotesHandler(DefaultConnection):
    def __init__(self):
        super().__init__(POLLS_DATABASE_NAME)

        self.__polls_tables_creator = QuestionsTablesCreator()

    def is_votes_table_exists(self, poll_id: int) -> bool:
        if not isinstance(poll_id, int):
            raise TypeError('poll_id must be of type int.')

        try:
            self._cursor.execute(f"""SELECT true FROM votes_{poll_id}""", ())
            return True
        except OperationalError:
            return False

    def add_vote(self, poll_id: int, question_id: int, ip: str) -> None:
        if not self.is_votes_table_exists(poll_id):
            raise PollNotFound(poll_id)

        self._cursor.execute(f"""INSERT INTO votes_{poll_id} (question_id, vote, ip) VALUES (?, ?, ?)""",
                             (question_id, True, ip))
        self._connection.commit()

    def get_votes(self, poll_id: int) -> dict:
        if not self.is_votes_table_exists(poll_id):
            raise PollNotFound(poll_id)

        self._cursor.execute(f"""SELECT question_id, COUNT(*) FROM votes_{poll_id} GROUP BY question_id""",)

        return {question_id: count for question_id, count in self._cursor.fetchall()}

    def is_ip_already_voted(self, poll_id: int, ip: str) -> bool:
        if not self.is_votes_table_exists(poll_id):
            raise PollNotFound(poll_id)

        self._cursor.execute(f"""SELECT true FROM votes_{poll_id}
                                WHERE ip = ?""", (ip,))

        return bool(self._cursor.fetchone())
