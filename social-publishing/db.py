import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session


DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:////data/publishing.db")

engine = create_engine(
    DATABASE_URL,
    future=True,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = scoped_session(
    sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
)


class Base(DeclarativeBase):
    pass


def init_db() -> None:
    from models import OAuthCredential, Post, Batch  # noqa: F401

    Base.metadata.create_all(bind=engine)
