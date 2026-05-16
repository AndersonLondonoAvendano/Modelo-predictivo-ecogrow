import uuid

from fastapi import APIRouter, Depends, Request, Response, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from backend.app.core.database import DBSession
from backend.app.core.limiter import limiter
from backend.app.services.auth_service import create_user, get_user_by_email, delete_user, get_all_users
from backend.app.schemas.auth_schema import UserCreate, UserResponse
from backend.app.auth.auth_service import new_login, refresh_session
from backend.app.auth.dependencies import CurrentUser, RequiereAdmin

router = APIRouter()

@router.get("/users/me", response_model=UserResponse, summary="Usuario actual")
def get_me(current_user: CurrentUser):
    return current_user

@router.get("/all/users", response_model=list[UserResponse], summary="Listar usuarios")
def get_users(current_user: RequiereAdmin, db: DBSession, skip: int = 0, limit: int = 200):
    return get_all_users(db, current_user, skip=skip, limit=limit)

@router.get("/users/{email}", response_model=UserResponse, summary="Buscar por email")
def get_user(email: str, current_user: RequiereAdmin, db: DBSession):
    return get_user_by_email(db, email)

@router.post("/login", summary="Iniciar sesión")
@limiter.limit("5/minute")
def login(request: Request, response: Response, db: DBSession, form_data: OAuth2PasswordRequestForm = Depends()):
    return new_login(form_data, db, response)

@router.post("/logout", summary="Cerrar sesión")
def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
    return {"message": "Sesión cerrada"}


@router.post("/refresh", summary="Renovar sesión")
@limiter.limit("10/minute")
def refresh(request: Request, response: Response, db: DBSession):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="No hay sesión activa")
    return refresh_session(token, response, db)

@router.post("/users", response_model=UserResponse, status_code=201, summary="Crear cuenta")
@limiter.limit("3/minute")
def create_account(user: UserCreate, db: DBSession, request: Request, response: Response):
    return create_user(db, user)

@router.delete("/users/{user_id}", summary="Eliminar usuario")
def remove_user(user_id: uuid.UUID, current_user: RequiereAdmin, db: DBSession):
    return delete_user(db, user_id, current_user)