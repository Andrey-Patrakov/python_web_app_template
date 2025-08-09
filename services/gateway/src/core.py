import functools
from importlib import import_module
from fastapi import Request, Response, HTTPException, status
from starlette.datastructures import UploadFile
from aiohttp.client_exceptions import ClientConnectorError, ContentTypeError

from .network import make_request, get_file_writer
from src.config import settings


SERVICE_HEADERS = ['Set-Cookie']


def route(
        request_method,
        path: str,
        status_code: int,
        payload_key: str,
        service_url: str,
        response_model: str = None,
        response_list: bool = False,
        authentication_required: bool = False):

    if response_model:
        response_model = import_function(response_model)
        if response_list:
            response_model = list[response_model]

    app_any = request_method(
        path, status_code=status_code, response_model=response_model)

    def wrapper(f):
        @app_any
        @functools.wraps(f)
        async def inner(request: Request, response: Response, **kwargs):

            scope = request.scope

            method = scope['method'].lower()
            path = scope['path']
            url = f'{service_url}{path}'

            payload_obj = kwargs.get(payload_key)
            if type(payload_obj) is UploadFile:
                writer = get_file_writer(file=payload_obj, name=payload_key)
                payload = None
            else:
                writer = None
                payload = payload_obj.dict() if payload_obj else {}

            if authentication_required:
                user_service_url = settings.SERVICES['users']['url']
                users_data, users_response = await make_request(
                    url=f'{user_service_url}{settings.USERS_SERVICE_PREFIX}/',
                    method='get',
                    cookies=request.cookies,
                    json_data={})

                if users_response.status >= 400:
                    raise HTTPException(
                        detail=users_data.get('detail', 'Service error.'),
                        status_code=users_response.status)

                if payload is not None:
                    payload = payload | users_data

            try:
                response_data, service_response = await make_request(
                    url=url,
                    method=method,
                    json_data=payload,
                    data=writer,
                    cookies=request.cookies)

                if service_response.status >= 400:
                    raise HTTPException(
                        detail=response_data.get('detail', 'Service error.'),
                        status_code=service_response.status)

            except ClientConnectorError:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail='Service is unavailable.',
                    headers={'WWW-Authenticate': 'Bearer'})

            except ContentTypeError:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail='Service error.',
                    headers={'WWW-Authenticate': 'Bearer'})

            response.status_code = service_response.status
            for key, value in service_response.headers.items():
                if key not in SERVICE_HEADERS:
                    continue

                response.headers.append(key, value)

            return response_data

    return wrapper


def import_function(method_path):
    module, method = method_path.rsplit('.', 1)
    mod = import_module(module)
    return getattr(mod, method, lambda *args, **kwargs: None)
