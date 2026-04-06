import bcrypt
from db import users_collection


def register_user(username: str, password: str) -> bool:
    """
    Registers a new user.
    Returns True on success, False if the username is already taken.
    """
    username = username.strip().lower()   # normalise: trim spaces & lowercase

    if users_collection.find_one({"username": username}):
        return False  # username already exists

    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    users_collection.insert_one({
        "username": username,
        "password": hashed_pw,
    })
    return True


def login_user(username: str, password: str) -> bool:
    """
    Validates login credentials.
    Returns True if the username exists and the password matches, else False.
    """
    username = username.strip().lower()   # same normalisation as registration

    user = users_collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return True
    return False