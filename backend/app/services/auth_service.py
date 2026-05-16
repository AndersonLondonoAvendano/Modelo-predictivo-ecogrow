from typing import Sequence
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import EmailStr

from backend.app.models.user import User
from backend.app.schemas.auth_schema import UserCreate
from backend.app.auth.hashing import hash_password



def get_all_users(db: Session, current_user: User, skip: int = 0, limit: int = 200) -> Sequence[User]:
    stmt = select(User).offset(skip).limit(limit)
    users = db.execute(stmt).scalars().all()
    return users


def get_user_by_email(db: Session, email: EmailStr) -> User:
    stmt = select(User).where(User.email == email)
    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"El usuario con email {email} no existe"
        )
    return user


def create_user(db: Session, user_data: UserCreate) -> User:
    stmt = select(User).where(User.email == user_data.email)
    existing = db.execute(stmt).scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un usuario con ese identificador"
        )

    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def delete_user(db: Session, user_id: uuid.UUID, current_user: User) -> User:
    if user_id == current_user.id:
        raise HTTPException(
            status_code=404,
            detail="No puedes eliminar tu propio usuario"
        )

    stmt = select(User).where(User.id == user_id)
    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    db.delete(user)
    db.commit()
    return user