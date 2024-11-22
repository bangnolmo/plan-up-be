from fastapi import APIRouter
from app.domain.oauth.google import google_router

router = APIRouter(
    prefix='/oauth'
)

router.include_router(google_router.router)
