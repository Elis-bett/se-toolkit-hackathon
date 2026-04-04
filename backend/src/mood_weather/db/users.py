"""Database operations for users."""

from typing import Optional

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from mood_weather.models.user import User, UserCreate


async def create_user(session: AsyncSession, user_data: UserCreate) -> User:
    """Create a new user."""
    user = User.model_validate(user_data)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_users(
    session: AsyncSession,
    limit: int = 100,
    offset: int = 0,
) -> list[User]:
    """Get all users with pagination."""
    stmt = select(User).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_user_by_external_id(
    session: AsyncSession,
    external_id: str,
) -> Optional[User]:
    """Get a user by their external ID."""
    stmt = select(User).where(User.external_id == external_id)
    result = await session.execute(stmt)
    return result.scalars().first()
