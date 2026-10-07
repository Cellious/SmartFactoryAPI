from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import get_current_user, require_role
from app.schemas.auth import LoginRequest, Token, User
from app.services.auth_service import login_user


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=Token,
)
def login(request: LoginRequest):
    token = login_user(
        request.username,
        request.password,
    )

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    return token


@router.get(
    "/me",
    response_model=User,
)
def get_me(current_user=Depends(get_current_user)):
    return current_user


@router.get(
    "/admin-only",
)
def admin_only(
    current_user=Depends(require_role("ADMIN")),
):
    return {
        "message": "Admin access granted",
        "username": current_user["username"],
        "role": current_user["role"],
    }


@router.get(
    "/production-access",
)
def production_access(
    current_user=Depends(
        require_role("ADMIN", "OPERATOR")
    ),
):
    return {
        "message": "Production access granted",
        "username": current_user["username"],
        "role": current_user["role"],
    }
