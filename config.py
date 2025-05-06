from user_exceptions import *

POLLS_DATABASE_NAME = "polls.db"
USERS_DATABASE_NAME = "users.db"
USERS_VOTES_DATABASE_NAME = "users_votes.db"


def PASSWORD_VERIFIER(password: str) -> None:
    if len(password) < 8:
        raise UserPasswordTooShortError()
    elif len(password) > 16:
        raise UserPasswordTooLongError()

def EMAIL_VERIFIER(email: str) -> None:
    if not email.count("@"):
        raise UserInvalidEmailError("Email must contain @ symbol.")
    elif len(email) > 35:
        raise UserTooLongEmailError()


def PHONE_NUMBER_VERIFIER(phone: str) -> None:
    if len(phone) < 11:
        raise UserInvalidPhoneNumberError()
    elif len(phone) > 13:
        raise UserInvalidPhoneNumberError()