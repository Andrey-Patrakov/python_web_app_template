from fastapi import HTTPException, status


class ContentSizeLimitMiddleware:

    def __init__(
            self, app, max_content_size: int | None = None):

        self.app = app
        self.max_content_size = max_content_size

    def receive_wrapper(self, receive):
        received = 0

        async def inner():
            nonlocal received
            message = await receive()
            if message["type"] != 'http.request':
                return message

            if self.max_content_size is None:
                return message

            body_len = len(message.get("body", b""))
            received += body_len
            if received > self.max_content_size:
                error_message = 'Невозможно загрузить файл. '
                error_message += 'Размер файла превышет '
                error_message += f'{int(self.max_content_size / 1024**2)}МБ'
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=error_message
                    )

            return message

        return inner

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        wrapper = self.receive_wrapper(receive)
        await self.app(scope, wrapper, send)
