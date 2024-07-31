from fastapi import FastAPI, Request
import psycopg2
from core.config import settings
from fastapi.exceptions import RequestValidationError
from api.v1.api_register import userRouter
from fastapi.responses import RedirectResponse
from models.user_model import base
from core.utils import responses
from core.database import engine
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

app = FastAPI()

# Database connection parameters from settings
DB_PASSWORD = settings.DB_PASSWORD
DB_HOST = settings.DB_HOST
DB_USER = settings.DB_USER
DATABASE_NAME = settings.DB_NAME
DB_PORT = settings.DB_PORT


def create_database_if_not_exists():
    """
    Connects to PostgreSQL, checks if the specified database exists,
    and creates it if it doesn't. Also creates the necessary tables.
    """
    conn = psycopg2.connect(dbname = "postgres", user = DB_USER, password = DB_PASSWORD, host = DB_HOST, port = DB_PORT)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # Allows database creation without a transaction
    cursor = conn.cursor()
    print("Creating the database...")

    # Check if the database already exists
    cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DATABASE_NAME}'")
    exists = cursor.fetchone()
    if not exists:
        # Create the database if it does not exist
        cursor.execute(f'CREATE DATABASE {DATABASE_NAME}')
        print(f"Database {DATABASE_NAME} created.")

    # Create tables if they do not exist
    base.metadata.create_all(bind = engine)

    cursor.close()
    conn.close()


# Event handler for application startup
@app.on_event("startup")
async def startup():
    """
    Event handler that runs on application startup.
    Calls the function to create the database and tables if they do not exist.
    """
    print("Starting up application...")
    create_database_if_not_exists()


# Include user-related routes
app.include_router(userRouter, prefix = "/api/v1")


@app.exception_handler(RequestValidationError)
async def handle_request_error(request: Request, exc: RequestValidationError):
    """
    Custom exception handler for request validation errors.

    Converts the validation errors into a list of dictionaries.
    - **request**: The request that caused the exception.
    - **exc**: The exception instance.

    Returns:
    - A JSON response containing the validation errors with a 422 status code.
    """
    errors = []
    for error in exc.errors():
        errors.append({ error['loc'][-1]: error['msg'] })
    return await responses(status_code = 422, error = errors)


@app.get("/")
async def redirect_url():
    """
    Redirects the root URL to the API documentation page.

    Returns:
    - A redirect response to the /docs endpoint.
    """
    return RedirectResponse(url = "/docs")
