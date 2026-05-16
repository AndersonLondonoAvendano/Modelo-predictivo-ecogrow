from typing import Annotated

from fastapi import HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from jose import ExpiredSignatureError, jwt, JWTError

from backend.app.core.config import settings
from backend.app.models.user import User
from backend.app.models.enums.user import UserStatus
from backend.app.core.database import DBSession


Oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", auto_error=False)


def _extract_token(request: Request) -> str | None:
    token = request.cookies.get("access_token")
    if token:
        return token
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth[7:]
    return None


def get_current_user(request: Request, db: DBSession, _token_schema: str | None = Depends(Oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="No autenticado")

    token = _extract_token(request)
    if not token:
        token = _token_schema

    if not token:
        raise credentials_exception

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str | None = payload.get("sub")
        token_type: str | None = payload.get("type")

        if not email or not isinstance(email, str) or token_type != "access":
            raise credentials_exception
        
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    
    except JWTError:
        raise credentials_exception

    stmt = select(User).where(User.email == email)
    user = db.execute(stmt).scalar_one_or_none()

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Usuario inactivo")

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_role(*roles: UserStatus):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            
            raise HTTPException(status_code=403, detail="No tienes permisos para esta acción")
        return current_user
    return role_checker


RequiereAdmin = Annotated[User, Depends(require_role(UserStatus.admin))]