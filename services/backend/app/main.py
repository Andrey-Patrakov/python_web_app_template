from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.users import router as users_router

# uvicorn app.main:app --reload
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.BACKEND_URL, settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home_page():
    return {'message': 'Привет мир!'}


app.include_router(users_router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
