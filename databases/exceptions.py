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
    def __init__(self, poll_id_or_name: int | str):
        super().__init__(f"Poll {poll_id_or_name} not found.")

class IPAlreadyVoted(DatabaseException):
    def __init__(self, ip: str):
        super().__init__(f"IP {ip} already voted.")