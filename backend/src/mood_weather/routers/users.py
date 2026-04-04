"""Users router with list and create endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from mood_weather.database import get_session
from mood_weather.models.user import UserCreate, UserRead
from mood_weather.db.users import create_user, get_users, get_user_by_external_id

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserRead])
async def list_users(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session),
) -> list[UserRead]:
    """List all users."""
    return await get_users(session, limit=limit, offset=offset)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    """Create a new user."""
    existing = await get_user_by_external_id(session, external_id=user_data.external_id)
    if existing:
        raise HTTPException(
            status_code=409,
            detail="User with this external_id already exists",
        )

    user = await create_user(session, user_data)
    return user
