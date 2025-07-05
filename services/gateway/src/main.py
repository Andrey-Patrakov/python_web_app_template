from fastapi import FastAPI, Request, Response, status
from .core import route
from services.users.routes import router as users_router
from fastapi.middleware.cors import CORSMiddleware
from .config import get_allowed_hosts


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_hosts(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)


@route(
    request_method=app.get,
    path='/',
    status_code=status.HTTP_200_OK,
    payload_key=None,
    service_url='http://backend:8000',
    response_model=None)
async def home_page(request: Request, response: Response):
    pass


app.include_router(users_router)
