from sqlalchemy import Column, Text, Integer, String, ForeignKey
from core.database import base

class UserProfile(base):
    """
    Represents a user profile in the database.

    Attributes:
    - **user_id**: Unique identifier for the user, auto-incremented.
    - **name**: Name of the user (non-nullable).
    - **email**: User's email address, unique and non-nullable.
    - **location**: Location of the user (non-nullable).
    - **about**: Optional text field for additional information about the user.
    - **password**: Hashed password of the user (non-nullable).
    """
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=False)
    about = Column(Text, nullable=True)
    password = Column(String, nullable=False)


class RefreshAccessTokens(base):
    """
    Represents the refresh tokens associated with a user.

    Attributes:
    - **tokenid**: Unique identifier for the refresh token, auto-incremented.
    - **tokens**: The refresh token itself, unique.
    - **type**: Type of token (default is "Bearer").
    - **user_id**: Foreign key linking to the user who owns this refresh token.
    """
    __tablename__ = 'refreshaccesstokens'

    tokenid = Column(Integer, primary_key=True, autoincrement=True, index=True)
    tokens = Column(Text, unique=True)
    type = Column(String, default="Bearer")
    user_id = Column(Integer, ForeignKey('users.user_id'))
