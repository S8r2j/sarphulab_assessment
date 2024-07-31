from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from schemas.token_schema import AccessToken, RefreshToken


class UserBasicInfo(BaseModel):
    """
    Basic information about a user.

    Attributes:
    - **name**: The user's name (required, cannot be empty).
    - **email**: The user's email address (required, must be a valid email).
    - **about**: Optional information about the user.
    - **location**: The user's location (required, cannot be empty).
    """
    name: str = Field(..., description = "Name of user")
    email: EmailStr = Field(..., description = "Email of user")
    about: Optional[str] = Field(None, description = "User information")
    location: str = Field(..., description = "Location")

    @field_validator('name', 'location')
    def not_empty(cls, v, info):
        """
        Ensure that fields are not empty or only whitespace.

        - **v**: The value of the field being validated.
        - **info**: Field validation metadata.

        Raises:
        - ValueError: If the field value is empty or only whitespace.
        """
        if not v.strip():
            raise ValueError(f'{info.field_name.capitalize()} cannot be empty.')
        return v

    class Config:
        # Automatically strip whitespace from string fields
        str_strip_whitespace = True


class UserProfile(UserBasicInfo):
    """
    User profile including password information.

    Attributes:
    - **password**: The user's password (required, cannot be empty).
    """
    password: str = Field(..., description = "Password provided by user")

    @field_validator('password')
    def pwd_not_empty(cls, v, info):
        """
        Ensure that the password field is not empty or only whitespace.

        - **v**: The value of the field being validated.
        - **info**: Field validation metadata.

        Raises:
        - ValueError: If the password value is empty or only whitespace.
        """
        if not v.strip():
            raise ValueError(f'{info.field_name.capitalize()} cannot be empty.')
        return v

    class Config:
        # Automatically strip whitespace from string fields
        str_strip_whitespace = True


class Login(BaseModel):
    """
    Schema for user login information.

    Attributes:
    - **email**: The user's email address (must be a valid email).
    - **password**: The user's password.
    """
    email: EmailStr
    password: str


class User(UserBasicInfo):
    """
    User information including authentication tokens.

    Attributes:
    - **user_token**: Refresh token for the user.
    """
    user_token: RefreshToken
