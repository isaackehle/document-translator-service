"""Authentication API endpoints."""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.security import create_access_token
from app.schemas.user import User, UserCreate
from app.services.user_service import user_service

router = APIRouter()


@router.post("/login", summary="Login and get access token", response_model=dict)
async def login(db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    """
    OAuth2 compatible token login.

    Args:
        db: Database session
        form_data: OAuth2 form data (username/email and password)

    Returns:
        dict: Access token and token type

    Raises:
        HTTPException: 400 if authentication fails
    """
    # Try to authenticate user
    user = await user_service.authenticate(db, email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.id}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/register",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)) -> User:
    """
    Register a new user.

    Args:
        user_in: User registration data
        db: Database session

    Returns:
        User: Created user

    Raises:
        HTTPException: 400 if email already exists
    """
    try:
        user = await user_service.create_user(db, user_in)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
