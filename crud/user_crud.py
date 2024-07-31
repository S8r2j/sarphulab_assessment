import psycopg2
from core.database import engine
from schemas import user_schema, token_schema
from models import user_model
from sqlalchemy.orm import Session
from core.utils import responses
from psycopg2 import OperationalError
from core.security import (
    verify_password, create_access_token, get_hash_password,
    create_refresh_access_token, get_current_user, get_current_user_from_refresh_token
)

# Aliases for easier reference
db_user = user_model.UserProfile
schema_user = user_schema.UserProfile


class CRUD:
    async def create_new_user(self, user: schema_user, db: Session):
        """
        Create a new user in the database.

        - **user**: UserProfile schema containing user data.
        - **db**: SQLAlchemy database session.

        Returns:
        - A JSONResponse indicating the result of the operation.
        """
        try:
            # Check if the user already exists
            existing_user = db.query(db_user).filter(db_user.email == user.email).one_or_none()
            if existing_user:
                return await responses(
                    status_code = 400, error = { "email": "Email already registered. Try logging in." }
                    )

            # Hash the user's password and create a new user profile
            hashed_password = await get_hash_password(password = user.password)
            db_object = user_model.UserProfile(
                name = user.name, email = user.email, location = user.location, about = user.about,
                password = hashed_password
            )
            db.add(db_object)
            db.commit()
            db.refresh(db_object)
            return await responses(message = "User created successfully.", status_code = 201)
        except psycopg2.Error as e:
            db.rollback()
            return await responses(status_code = 500, error = { "Database Error": str(e) })
        except Exception as e:
            db.rollback()
            return await responses(status_code = 500, error = { "error": str(e) })

    async def authenticate_user(self, loginInfo: user_schema.Login, db: Session) -> user_schema.User:
        """
        Authenticate a user and generate access and refresh tokens.

        - **loginInfo**: Login schema containing user login details.
        - **db**: SQLAlchemy database session.

        Returns:
        - A JSONResponse with login status and user data.
        """
        try:
            # Retrieve the user from the database
            existing_user = db.query(db_user).filter(db_user.email == loginInfo.email).one_or_none()
            if not existing_user:
                return await responses(
                    status_code = 404, error = { "error": "User not found. Try creating an account." }
                    )

            # Verify the provided password
            is_authorized = await verify_password(loginInfo.password, existing_user.password)
            if not is_authorized:
                return await responses(
                    status_code = 401, error = { "error": "Invalid credentials. Try again..." }
                )

            # Check if a refresh token exists for the user, create one if not
            check_refresh_token = db.query(user_model.RefreshAccessTokens).join(user_model.UserProfile).filter(
                user_model.UserProfile.user_id == existing_user.user_id
            ).one_or_none()
            if not check_refresh_token:
                refresh_token = await create_refresh_access_token(data = { "id": existing_user.user_id })
                print("refresh token: ", refresh_token)
                db_refresh_token = user_model.RefreshAccessTokens(
                    tokens = refresh_token, user_id = existing_user.user_id
                    )
                db.add(db_refresh_token)
                db.commit()
                db.refresh(db_refresh_token)
                check_refresh_token = db_refresh_token

            print(check_refresh_token.tokens)

            # Generate access token
            access_token = await create_access_token(data = { "id": existing_user.user_id })
            token = token_schema.RefreshToken(token = access_token, refreshToken = check_refresh_token.tokens)

            # Return the user data and tokens
            user = user_schema.User(
                name = existing_user.name, location = existing_user.location, email = existing_user.email,
                about = existing_user.about, user_token = token
            )
            return await responses(message = "Login successful.", status_code = 200, data = user.dict())
        except Exception as e:
            return await responses(status_code = 500, error = { "error": str(e) })

    async def refresh_expired_token(self, token: token_schema.AccessToken, db: Session):
        """
        Refresh an expired access token using a refresh token.

        - **token**: AccessToken schema containing the refresh token.
        - **db**: SQLAlchemy database session.

        Returns:
        - A JSONResponse with the new access token and user data.
        """
        try:
            # Get the current user based on the refresh token
            current_user = await get_current_user_from_refresh_token(token = token.token, db = db)
            if not current_user:
                return await responses(status_code = 404, error = { "error": "No user found." })

            # Check if the refresh token exists in the database
            token_check_in_db = db.query(user_model.RefreshAccessTokens).join(user_model.UserProfile).filter(
                user_model.UserProfile.user_id == current_user.user_id
            ).one_or_none()
            if not token_check_in_db:
                return await responses(status_code = 401, error = { "error": "Authorization failed. Log in again." })

            # Generate a new access token
            refreshed_token = await create_access_token(data = { "id": current_user.user_id })
            token = user_schema.RefreshToken(token = refreshed_token, refreshToken = token.token)

            # Return the user data and new token
            user = user_schema.User(
                name = current_user.name, location = current_user.location, email = current_user.email,
                about = current_user.about, user_token = token.dict()
            )
            return await responses(message = "Login successful.", status_code = 200, data = user.dict())
        except Exception as e:
            return await responses(
                status_code = 500, error = { "error": f"Failed to refresh the token. Please log in again. {e}" }
                )
