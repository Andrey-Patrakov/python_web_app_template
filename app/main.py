from fastapi import FastAPI
from app.users import router as users_router

# uvicorn app.main:app --reload
app = FastAPI()


@app.get('/')
def home_page():
    return {'message': 'Привет мир!'}


app.include_router(users_router)
