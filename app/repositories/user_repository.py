from app.database.fake_db import users


def get_user_by_username(username: str):
    for user in users:
        if user["username"] == username:
            return user

    return None
