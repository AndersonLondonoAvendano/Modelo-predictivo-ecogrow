from fastapi import HTTPException, Response
from sqlalchemy.orm import Session
from jose import ExpiredSignatureError, jwt, JWTError
from sqlalchemy import select

from backend.app.core.config import settings
from backend.app.models.user import User
from backend.app.auth.jwt_handler import create_access_token, create_refresh_token
from backend.app.auth.hashing import verify_password
from backend.app.services.auth_service import get_user_by_email


def _set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    is_dev = settings.ENV.lower() in ("dev", "development")
    secure = not is_dev

    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,
        secure=secure,
        samesite="lax",
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
        httponly=True,
        secure=secure,
        samesite="lax",
        path="/",
    )


def authenticate_user(db: Session, email: str, password: str) -> User:
    result = db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    return user


def new_login(form_data, db: Session, response: Response):
    db_user = authenticate_user(db, form_data.username, form_data.password)

    access_token = create_access_token({"sub": db_user.email})
    refresh_token = create_refresh_token({"sub": db_user.email})
    _set_auth_cookies(response, access_token, refresh_token)


    return {
        "access_token": access_token,
        "user": {
            "id": str(db_user.id),
            "email": db_user.email,
            "role": db_user.role,
        }
    }


def refresh_session(refresh_token: str, response: Response, db: Session):
    credentials_exception = HTTPException(status_code=401, detail="Sesión expirada")
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        email: str | None = payload.get("sub")
        token_type: str | None = payload.get("type")

        if not email or token_type != "refresh":
            raise credentials_exception

    except ExpiredSignatureError:
        raise credentials_exception
    
    except JWTError:
        raise credentials_exception

    stmt = select(User).where(User.email == email)
    result = db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if not existing_user or not existing_user.is_active:
        raise credentials_exception

    new_access = create_access_token({"sub": existing_user.email})
    new_refresh = create_refresh_token({"sub": existing_user.email})
    _set_auth_cookies(response, new_access, new_refresh)

    return {"message": "Sesión renovada"}