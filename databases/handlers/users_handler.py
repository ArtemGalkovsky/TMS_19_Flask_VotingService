from databases.default_connection_class import DefaultConnection
from databases.creators.users_tables_creator import Creator as UsersTablesCreator
from databases.exceptions import UserAlreadyExists, UserNotExist
from config import USERS_DATABASE_NAME, EMAIL_VERIFIER, PASSWORD_VERIFIER, PHONE_NUMBER_VERIFIER

class UsersHandler(DefaultConnection):
    def __init__(self):
        super().__init__(USERS_DATABASE_NAME)

        self.__polls_tables_creator = UsersTablesCreator(initial_tables_auto_creation=True)

    def is_user_exists(self, username: str) -> bool:
        self._cursor.execute("""SELECT true
                                FROM users
                                WHERE username = ?""", (username,))

        if self._cursor.fetchone():
            return True

        return False

    def add_user(self, username: str, email: str, phone_number: str, password: str) -> None:
        if self.is_user_exists(username):
            raise UserAlreadyExists(username)

        self._cursor.execute("""INSERT INTO users (username, email, phone_number, password)VALUES (?, ?, ?, ?)""",
                             (username, email, phone_number, password))
        self._connection.commit()

    def update_user(self, username_to_update: str, *, new_email: str | None = None,
                    new_phone_number: str | None = None, new_password: str | None = None) -> None:
        if not self.is_user_exists(username_to_update):
            raise UserNotExist(username_to_update)

        to_update = dict()
        for column, data, verifier in zip(("email", "phone_number", "password"),
                                          (new_email, new_phone_number, new_password),
                                          (EMAIL_VERIFIER, PHONE_NUMBER_VERIFIER, PASSWORD_VERIFIER)):
            verifier(data)

            to_update[column] = data

        update_string = ", ".join(f"{column} = ?" for column in to_update.keys())
        self._cursor.execute(f"""UPDATE users SET {update_string} WHERE username = ?""",
                             (username_to_update,) + tuple(to_update.values()))
        self._connection.commit()


if __name__ == '__main__':
    handler = UsersHandler()

    # handler.add_user("Artem", "@com", "1234567890123", "12344567")
    # handler.add_user("Artem", 1, 1, 1)

    handler.update_user("Artem", new_email="<EMAIL@>", new_phone_number="0123456789111", new_password="<PASSWORD>")