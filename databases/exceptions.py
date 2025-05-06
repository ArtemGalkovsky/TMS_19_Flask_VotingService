class DatabaseException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class TableAlreadyExists(DatabaseException):
    def __init__(self, table_name: str):
        super().__init__(f"Table '{table_name}' already exists.")

class PollAlreadyExists(DatabaseException):
    def __init__(self, poll_name: str):
        super().__init__(f"Poll '{poll_name}' already exists.")

class PollNotFound(DatabaseException):
    def __init__(self, poll_id: int):
        super().__init__(f"Poll {poll_id} not found.")

class UserAlreadyExists(DatabaseException):
    def __init__(self, username: str):
        super().__init__(f"User '{username}' already exists.")

class UserNotExist(DatabaseException):
    def __init__(self, username: str):
        super().__init__(f"User '{username}' does not exist.")

class UserAlreadyVoted(DatabaseException):
    def __init__(self, username: str):
        super().__init__(f"User '{username}' already voted.")