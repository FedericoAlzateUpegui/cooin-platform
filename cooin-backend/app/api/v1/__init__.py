from fastapi import APIRouter

from app.api.v1 import auth, profiles, connections

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
api_router.include_router(connections.router, prefix="/connections", tags=["connections"])