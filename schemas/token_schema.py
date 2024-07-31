from pydantic import BaseModel

class TokenData(BaseModel):
    """
    Represents the data contained in a token.

    Attributes:
    - **id**: The unique identifier for the user associated with the token.
    """
    id: int

class AccessToken(BaseModel):
    """
    Represents an access token.

    Attributes:
    - **token**: The actual access token string.
    - **tokenType**: The type of token (default is "Bearer").
    """
    token: str
    tokenType: str = "Bearer"

class RefreshToken(AccessToken):
    """
    Represents a refresh token, extending the AccessToken.

    Attributes:
    - **refreshToken**: The refresh token string.
    """
    refreshToken: str
