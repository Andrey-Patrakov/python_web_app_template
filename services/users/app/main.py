from fastapi import FastAPI
from app.users.routes import router as user_router

app = FastAPI()


@app.get('/api/users/')
def get_current_user():
    return {'message': 'Привет мир!'}


app.include_router(user_router)
