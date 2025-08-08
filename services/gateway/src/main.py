from fastapi import FastAPI

from services.storage.routes import router as storage_router
from services.users.routes import router as users_router

from fastapi.middleware.cors import CORSMiddleware
from src.middleware import ContentSizeLimitMiddleware
from src.config import settings, get_allowed_hosts
from src.lifespan import lifespan


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_hosts(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

app.add_middleware(
    ContentSizeLimitMiddleware,
    max_content_size=settings.FILE_MAX_LENGTH)


app.include_router(storage_router)
app.include_router(users_router)
