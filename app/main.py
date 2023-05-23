from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

from users.api.v1 import router as users_router


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME, version='0.2.0')

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(users_router)

    return _app


app = get_application()
