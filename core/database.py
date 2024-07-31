from .config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Extract database configuration values from settings
password = settings.DB_PASSWORD
host = settings.DB_HOST
user = settings.DB_USER
database = settings.DB_NAME
port = settings.DB_PORT

# Construct the database URL for PostgreSQL using the settings
database_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

# Create an SQLAlchemy engine with connection pooling and automatic pre-ping to detect stale connections
engine = create_engine(database_url, pool_pre_ping=True)

# Create a session factory bound to the engine, with autocommit disabled
session = sessionmaker(autocommit=False, bind=engine)

# Define a base class for declarative class definitions
base = declarative_base()

def get_db():
    """
    Dependency to provide a SQLAlchemy database session.

    Yields:
    - A database session that can be used within a request, and ensures that the session is closed
      after the request is completed.

    Usage:
    - Can be used as a dependency in FastAPI route handlers to get a database session.
    """
    db = session()
    try:
        yield db
    finally:
        db.close()
