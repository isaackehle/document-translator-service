"""User API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.schemas.user import User, UserCreate, UserUpdate
from app.services.user_service import user_service

router = APIRouter()


@router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Create new user",
)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)) -> User:
    """
    Create a new user.

    Args:
        user_in: User creation data
        db: Database session

    Returns:
        User: Created user

    Raises:
        HTTPException: 400 if user already exists
    """
    try:
        user = await user_service.create_user(db, user_in)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/me", response_model=User, summary="Get current user")
async def read_current_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get current authenticated user.

    Returns:
        User: Current user
    """
    return current_user


@router.get("/{user_id}", response_model=User, summary="Get user by ID")
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> User:
    """
    Get user by ID.

    Args:
        user_id: User ID
        db: Database session
        _current_user: Current authenticated user (used for auth only)

    Returns:
        User: User data

    Raises:
        HTTPException: 404 if user not found
    """
    user = await user_service.repository.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=User, summary="Update user")
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Update user.

    Args:
        user_id: User ID
        user_in: Update data
        db: Database session
        current_user: Current authenticated user

    Returns:
        User: Updated user

    Raises:
        HTTPException: 403 if not authorized, 404 if not found
    """
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    user = await user_service.update_user(db, user_id, user_in)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete user")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete user.

    Args:
        user_id: User ID
        db: Database session
        current_user: Current authenticated user

    Raises:
        HTTPException: 403 if not authorized, 404 if not found
    """
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    deleted = await user_service.repository.delete(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
