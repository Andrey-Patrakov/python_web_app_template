from fastapi import FastAPI
from app.lifespan import lifespan
from app.middleware import ContentSizeLimitMiddleware

from fastapi.middleware.cors import CORSMiddleware
from app.config import settings, get_allowed_hosts
from app.user.routes import router as user_router
from app.storage.routes import router as storage_router

# uvicorn app.main:app --reload
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_hosts(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

app.add_middleware(
    ContentSizeLimitMiddleware,
    max_content_size=settings.storage.FILE_MAX_LENGTH)


@app.get('/')
def home_page():
    return {'message': 'Привет мир!'}


app.include_router(user_router)
app.include_router(storage_router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
