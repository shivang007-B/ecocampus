from fastapi import APIRouter
from backend.api.v1.endpoints import auth, users, campus, carbon, iot

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(campus.router, prefix="/campuses", tags=["campuses"])
api_router.include_router(carbon.router, prefix="/carbon", tags=["carbon"])
api_router.include_router(iot.router, prefix="/iot", tags=["iot"])