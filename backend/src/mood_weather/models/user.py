"""User model for mood weather users."""

from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    """Shared fields for users."""

    external_id: str = Field(unique=True, index=True)
    display_name: str = Field(max_length=100)


class User(UserBase, table=True):
    """User table model."""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(UserBase):
    """Schema for creating a user."""


class UserRead(UserBase):
    """Schema for reading a user."""

    id: int
    created_at: datetime
