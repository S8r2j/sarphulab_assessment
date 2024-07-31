from fastapi import APIRouter
from .endpoints.user_api import userRouter

# Initialize a new APIRouter instance for version 1 of the API
v1router = APIRouter(tags=["USER"])

# Include the user-related router in the v1 router
# This allows the user-related endpoints to be accessible under the "/v1" prefix
v1router.include_router(userRouter)
