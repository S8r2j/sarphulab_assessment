from fastapi import APIRouter, Depends
from core.database import get_db
from crud.user_crud import CRUD
from sqlalchemy.orm import Session
from schemas.user_schema import UserProfile, Login, AccessToken, UserBasicInfo
from core.security import get_current_user

# Initialize a new APIRouter instance for user-related endpoints
userRouter = APIRouter()

@userRouter.post("/register-user")
async def create_user(userInfo: UserProfile, db: Session = Depends(get_db)):
    """
    Register a new user.

    This endpoint allows a user to register by providing their profile information.

    - **userInfo**: The profile information of the user to be created.

    Returns:
    - A response object containing the details of the created user.
    """
    user_crud = CRUD()
    response = await user_crud.create_new_user(db=db, user=userInfo)
    return response

@userRouter.post("/auth/login")
async def authenticate_user(loginInfo: Login, db: Session = Depends(get_db)):
    """
    Authenticate a user and obtain an access token.

    This endpoint is used for user login. It verifies user credentials and returns an access token if valid.

    - **loginInfo**: The login credentials of the user.

    Returns:
    - A response object containing the access token.
    """
    user_login = CRUD()
    response = await user_login.authenticate_user(loginInfo=loginInfo, db=db)
    return response

@userRouter.post("/auth/refresh-token")
async def get_refresh_token(token: AccessToken, db: Session = Depends(get_db)):
    """
    Refresh an expired access token.

    This endpoint allows a user to obtain a new access token using a refresh token.

    - **token**: The refresh token used to obtain a new access token.

    Returns:
    - A response object containing the new access token.
    """
    refreshToken = CRUD()
    response = await refreshToken.refresh_expired_token(token=token, db=db)
    return response

@userRouter.get("/me", dependencies=[Depends(get_current_user)], response_model=UserBasicInfo)
async def get_profile(user = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Retrieve the profile of the currently authenticated user.

    This endpoint returns the profile information of the currently logged-in user.

    Returns:
    - The profile information of the currently authenticated user.
    """
    return user
