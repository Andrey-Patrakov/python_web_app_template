from fastapi import Request, Response, HTTPException, status
from src.utils.jwt import AccessToken, RefreshToken
from src.utils.jwt import TokenError, TokenExpiredError
from src.services.tokens import TokenService, TokenTypes


class AuthService:

    def __init__(self, request: Request, response: Response):
        self.request = request
        self.response = response

    async def login(self, user_id: int):
        AccessToken(self.request, self.response).create({'sub': str(user_id)})
        RefreshToken(self.request, self.response).create({'sub': str(user_id)})

    async def logout(self):

        access_token = AccessToken(self.request, self.response)
        refresh_token = RefreshToken(self.request, self.response)

        for auth_token in (access_token, refresh_token):
            try:
                token = auth_token.read()
                token_data = auth_token.decode(token)
                user_id = token_data.get('sub')

                if user_id:
                    await TokenService().add(
                        token=token,
                        expires_delta=auth_token.expires_delta,
                        token_type=TokenTypes.BLACKLISTED,
                        user_id=user_id)

                auth_token.delete()

            except TokenError:
                pass

    async def get_current_user_id(self):
        access_token = AccessToken(self.request, self.response)

        try:
            try:
                token = access_token.read()
            except TokenExpiredError:
                await self.refresh_access_token()

            token = access_token.read()
            if await TokenService().exists(token):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='User is unauthorized.')

            return int(access_token.get('sub'))

        except TokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='User is unauthorized.')

    async def refresh_access_token(self):
        refresh_token = RefreshToken(self.request, self.response)

        token = refresh_token.read()
        if await TokenService().exists(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='User is unauthorized.')

        user_id = refresh_token.get('sub')
        access_token = AccessToken(self.request, self.response)
        return access_token.create({'sub': str(user_id)})
