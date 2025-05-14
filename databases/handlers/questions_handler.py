from databases.default_connection_class import DefaultConnection
from databases.creators.questions_tables_creator import Creator as QuestionsTablesCreator
from databases.exceptions import PollNotFound
from config import POLLS_DATABASE_NAME
from sqlite3 import OperationalError

class QuestionsHandler(DefaultConnection):
    def __init__(self):
        super().__init__(POLLS_DATABASE_NAME)

        self.__polls_tables_creator = QuestionsTablesCreator()

    def is_questions_table_exists(self, poll_id: int) -> bool:
        if not isinstance(poll_id, int):
            raise TypeError('poll_id must be of type int.')

        try:
            self._cursor.execute(f"""SELECT true FROM questions_{poll_id}""", ())
            return True
        except OperationalError:
            return False

    def add_question(self, poll_id: int, text: str) -> None:
        if not self.is_questions_table_exists(poll_id):
            raise PollNotFound(poll_id)

        self._cursor.execute(f"""INSERT INTO questions_{poll_id} (question_text) VALUES (?)""",
                             (text,))
        self._connection.commit()

    def update_question(self, poll_id: int, question_id_to_update: int, new_text: str) -> None:
        if not isinstance(question_id_to_update, int):
            raise TypeError('question_id_to_update must be of type int.')

        if not self.is_questions_table_exists(poll_id):
            raise PollNotFound(poll_id)

        self._cursor.execute(f"""UPDATE questions_{poll_id} SET question_text = ? WHERE question_id = ?""",
                             (question_id_to_update, new_text))
        self._connection.commit()

    def get_questions(self, poll_id: int) -> list:
        if not isinstance(poll_id, int):
            raise TypeError('poll_id must be of type int.')

        if not self.is_questions_table_exists(poll_id):
            raise PollNotFound(poll_id)

        self._cursor.execute(f"""SELECT question_id, question_text FROM questions_{poll_id}""")
        return self._cursor.fetchall()
