from fastapi import FastAPI, Request, Response, status
from .core import route


app = FastAPI()


@route(
    request_method=app.get,
    path='/',
    status_code=status.HTTP_200_OK,
    payload_key=None,
    service_url='http://backend:8000',
    response_model=None)
async def home_page(request: Request, response: Response):
    pass
