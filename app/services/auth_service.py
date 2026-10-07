from app.auth.security import (
    create_access_token,
    verify_password,
)

from app.repositories.user_repository import (
    get_user_by_username,
)


def authenticate_user(
    username: str,
    password: str,
):
    user = get_user_by_username(username)

    if user is None:
        return None

    if not user["active"]:
        return None

    if not verify_password(
        password,
        user["hashed_password"],
    ):
        return None

    return user


def login_user(
    username: str,
    password: str,
):
    user = authenticate_user(
        username,
        password,
    )

    if user is None:
        return None

    token = create_access_token(
        {
            "sub": str(user["id"]),
            "username": user["username"],
            "role": user["role"],
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }
