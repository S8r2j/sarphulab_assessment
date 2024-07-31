import json
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.config import settings
from jose import JWTError, jwt
from schemas.token_schema import TokenData
from models.user_model import UserProfile
from datetime import timedelta, datetime
from passlib.context import CryptContext
from fastapi.security.oauth2 import OAuth2PasswordBearer

# Initialize CryptContext for password hashing and verification
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token-based authentication
auth_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Secret key and algorithm for creating JWT access tokens
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.TOKEN_CREATION_ALGORITHM

# Expiry time of the access token in minutes
TOKEN_EXPIRY_MINUTES = settings.TOKEN_EXPIRY_LIMIT

async def create_access_token(data: dict):
    """
    Create a JWT access token.

    - **data**: Dictionary containing the payload data for the token.

    Returns:
    - The encoded JWT access token as a string.
    """
    data_encode = data.copy()

    # Set the expiration time for the access token
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRY_MINUTES)
    data_encode.update({"expiry time": json.dumps(expire, default=str)})

    # Encode the data into a JWT access token
    access_token = jwt.encode(data_encode, SECRET_KEY, algorithm=ALGORITHM)
    return access_token

async def create_refresh_access_token(data: dict):
    """
    Create a JWT refresh token.

    - **data**: Dictionary containing the payload data for the token.

    Returns:
    - The encoded JWT refresh token as a string.
    """
    data_encode = data.copy()

    # Encode the data into a JWT refresh token
    refresh_access_token = jwt.encode(data_encode, settings.REFRESH_TOKEN_SECRET, algorithm=ALGORITHM)
    return refresh_access_token

def verify_access_token(token: str, credentials_exception):
    """
    Verify and decode an access token.

    - **token**: JWT access token to verify.
    - **credentials_exception**: Exception to raise if the token is invalid.

    Returns:
    - The user ID extracted from the token.
    """
    try:
        # Decode the access token
        data_decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = data_decode.get("id")

        if not id:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data.id

async def verify_refresh_access_token(token: str, credentials_exception):
    """
    Verify and decode a refresh token.

    - **token**: JWT refresh token to verify.
    - **credentials_exception**: Exception to raise if the token is invalid.

    Returns:
    - The user ID extracted from the token.
    """
    try:
        # Decode the refresh token
        data_decode = jwt.decode(token, settings.REFRESH_TOKEN_SECRET, algorithms=[ALGORITHM])
        id: int = data_decode.get("id")

        if not id:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data.id

async def get_hash_password(password: str):
    """
    Hash a plaintext password.

    - **password**: The plaintext password to hash.

    Returns:
    - The hashed password.
    """
    return password_context.hash(password)

async def verify_password(plain_pwd, hash_pwd):
    """
    Verify a plaintext password against a hashed password.

    - **plain_pwd**: The plaintext password.
    - **hash_pwd**: The hashed password to compare against.

    Returns:
    - True if the password matches, False otherwise.
    """
    return password_context.verify(plain_pwd, hash_pwd)

def get_current_user(token: str = Depends(auth_scheme), db: Session = Depends(get_db)):
    """
    Get the currently authenticated user based on the access token.

    - **token**: The JWT access token provided in the request.
    - **db**: The database session dependency.

    Returns:
    - The UserProfile object for the currently authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token = verify_access_token(token, credentials_exception)
    user = db.query(UserProfile).filter(UserProfile.user_id == token).one_or_none()
    return user

async def get_current_user_from_refresh_token(token: str = Depends(auth_scheme), db: Session = Depends(get_db)):
    """
    Get the currently authenticated user based on the refresh token.

    - **token**: The JWT refresh token provided in the request.
    - **db**: The database session dependency.

    Returns:
    - The UserProfile object for the currently authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token = await verify_refresh_access_token(token, credentials_exception)
    user = db.query(UserProfile).filter(UserProfile.user_id == token).one_or_none()
    return user
