import functools
from importlib import import_module
from fastapi import Request, Response, HTTPException, status
from aiohttp.client_exceptions import ClientConnectorError, ContentTypeError

from .network import make_request


def route(
        request_method,
        path: str,
        status_code: int,
        payload_key: str,
        service_url: str,
        response_model: str = None,
        response_list: bool = False):

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
            payload = payload_obj.dict() if payload_obj else {}

            try:
                response_data, service_status_code = await make_request(
                    url=url,
                    method=method,
                    data=payload)

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

            response.status_code = service_status_code

            return response_data

    return wrapper


def import_function(method_path):
    module, method = method_path.rsplit('.', 1)
    mod = import_module(module)
    return getattr(mod, method, lambda *args, **kwargs: None)
