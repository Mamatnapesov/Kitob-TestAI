from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Text
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    String,
    Float,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.db import Base


# =====================================================
# BOOK
# =====================================================
class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    author: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    cover: Mapped[str] = mapped_column(
        String(300),
        default="",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    tests = relationship(
        "Test",
        back_populates="book",
        cascade="all, delete-orphan",
    )

    results = relationship(
        "Result",
        back_populates="book",
        cascade="all, delete-orphan",
    )
# =====================================================
# TEST
# =====================================================

class Test(Base):
    __tablename__ = "tests"

    id: Mapped[int] = mapped_column(primary_key=True)

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id"),
    )

    question: Mapped[str] = mapped_column(
        String(1000),
    )

    option_a: Mapped[str] = mapped_column(
        String(300),
    )

    option_b: Mapped[str] = mapped_column(
        String(300),
    )

    option_c: Mapped[str] = mapped_column(
        String(300),
    )

    option_d: Mapped[str] = mapped_column(
        String(300),
    )

    correct: Mapped[str] = mapped_column(
        String(1),
    )

    difficulty: Mapped[str] = mapped_column(
        String(20),
        default="easy",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    book = relationship(
        "Book",
        back_populates="tests",
    )


# =====================================================
# USER
# =====================================================

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    telegram_id: Mapped[int] = mapped_column(
        unique=True,
        index=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
    )

    username: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    results = relationship(
        "Result",
        back_populates="user",
        cascade="all, delete-orphan",
    )


# =====================================================
# RESULT
# =====================================================

class Result(Base):
    __tablename__ = "results"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id"),
        nullable=False,
    )

    total: Mapped[int] = mapped_column(
        default=0,
    )

    correct: Mapped[int] = mapped_column(
        default=0,
    )

    wrong: Mapped[int] = mapped_column(
        default=0,
    )

    percent: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    spent_time: Mapped[int] = mapped_column(
        default=0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    user = relationship(
        "User",
        back_populates="results",
    )

    book = relationship(
        "Book",
        back_populates="results",
    )