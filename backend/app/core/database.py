from typing import Generator, Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from backend.app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.ENV == "dev",
    connect_args={"options": "-c client_encoding=UTF8"},
    pool_size=10,          
    max_overflow=20,       
    pool_timeout=30,       
    pool_recycle=1800,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DBSession = Annotated[Session, Depends(get_db)]