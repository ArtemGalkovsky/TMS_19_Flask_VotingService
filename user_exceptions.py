class UserException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class UserInvalidPasswordError(UserException):
    def __init__(self, message: str):
        super().__init__(f"PASSWORD ERROR: {message}")

class UserPasswordTooShortError(UserInvalidPasswordError):
    def __init__(self):
        super().__init__("Password length is too short.")

class UserPasswordTooLongError(UserInvalidPasswordError):
    def __init__(self):
        super().__init__("Password is too long.")

class UserInvalidEmailError(UserException):
    def __init__(self, message: str):
        super().__init__(f"EMAIL ERROR: {message}")

class UserTooLongEmailError(UserInvalidEmailError):
    def __init__(self):
        super().__init__("Email too long.")

class UserInvalidPhoneNumberError(UserException):
    def __init__(self):
        super().__init__("Invalid phone number.")


