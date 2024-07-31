# FastAPI User Management Application

This FastAPI application provides a user management system with authentication and token handling. It uses PostgreSQL for database storage and implements JWT for managing user sessions.

## Features

- User registration
- User login
- Token-based authentication (access and refresh tokens)
- Secure password hashing
- Token expiration and refresh

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Exception Handling](#exception-handling)

## Installation

1. **Clone the repository.**

2. **Create and activate a virtual environment.**
    ```
   python -m venv venv
   source venv/bin/activate

3. **Install dependencies.**
    ```
   pip install -r requirements.txt 

4. **Set up environment variables.**

   Create a `.env` file in the root directory with the following content:

   ```env
   DB_NAME=db_name
   DB_USER=db_user
   DB_PORT=db_port
   DB_PASSWORD=db_password
   DB_HOST=db_host
   SECRET_KEY=your_secret_key
   TOKEN_CREATION_ALGORITHM=your_prefered_algorithm
   TOKEN_EXPIRY_LIMIT=prefered_number_of_days
   REFRESH_TOKEN_SECRET=your_secret_key

5. **Run the command:**
    ```
   uvicorn main:app --reload
6. **You can now access the APIs at**
   ```
   http://127.0.0.1:8000
   
## Configuration
The application uses pydantic_settings to manage configuration settings. Ensure you have all required environment variables set in your .env file.

## Usage
Run the application.

Access the API documentation at /docs or /redoc.

## API Endpoints

### User Registration

- **Endpoint:** `/api/v1/register-user`
- **Method:** POST
- **Description:** Register a new user.

### User Login

- **Endpoint:** `/api/v1/auth/login`
- **Method:** POST
- **Description:** Authenticate user and return access and refresh tokens.

### Token Refresh

- **Endpoint:** `/api/v1/auth/refresh-token`
- **Method:** POST
- **Description:** Refresh the access token using a valid refresh token.

### Get User Profile

- **Endpoint:** `/api/v1/me`
- **Method:** GET
- **Description:** Get the profile of the currently authenticated user.

## Database Schema

### `users` Table

- **user_id:** Integer, Primary Key
- **name:** String, Not Null
- **email:** String, Unique, Not Null
- **location:** String, Not Null
- **about:** Text, Nullable
- **password:** String, Not Null

### `refreshaccesstokens` Table

- **tokenid:** Integer, Primary Key
- **tokens:** Text, Unique
- **type:** String, Default "Bearer"
- **user_id:** Integer, Foreign Key to `users.user_id`

## Exception Handling
The application handles request validation errors and provides appropriate responses. Custom exception handling is implemented for request validation errors to return detailed error messages.
