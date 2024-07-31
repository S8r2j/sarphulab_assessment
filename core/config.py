from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configuration settings for the application.

    This class uses Pydantic's BaseSettings to read configuration from environment variables
    and validate them.
    """
    DB_NAME: str  # The name of the database
    DB_USER: str  # The username for database authentication
    DB_PORT: str  # The port on which the database is running
    DB_PASSWORD: str  # The password for database authentication
    DB_HOST: str  # The host address of the database server
    SECRET_KEY: str  # Secret key used for cryptographic operations, e.g., signing tokens
    TOKEN_CREATION_ALGORITHM: str  # Algorithm used for creating tokens (e.g., 'HS256')
    TOKEN_EXPIRY_LIMIT: int  # The expiry limit for access tokens in seconds
    REFRESH_TOKEN_SECRET: str  # Secret key used for creating and validating refresh tokens

    class Config:
        """
        Configuration class for Pydantic settings.

        - `env_file`: Specifies the environment file from which to load the settings.
        """
        env_file = ".env"

# Instantiate the settings object
settings = Settings()
