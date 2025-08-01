from pathlib import Path
from urllib.parse import urlparse, urlencode, urlunsplit
from jinja2 import Environment, FileSystemLoader

from src.config import settings
from src.models.users import User
from src.models.tokens import Token
from src.utils.mail import SMTP_Mail


class EmailService:

    def __init__(self):
        pass

    async def send_email_verification_message(self, user: User, token: Token):
        link, sitename = await self._get_confirmation_url(token.token)
        with SMTP_Mail() as mail:
            message = mail.message(
                addr_to=user.email,
                subject='Для завершения регистрации подтвердите свой email')

            message.attach_html(self._create_message(
                template='verify_email.html',
                link=link,
                sitename=sitename))

            print(self._create_message(
                template='verify_email.html',
                link=link,
                sitename=sitename))

            message.send()

    async def _get_confirmation_url(self, token_str: str):
        frontend_url = urlparse(
            f'{settings.FRONTEND_HOST}:{settings.FRONTEND_PORT}')

        path = 'user/confirmation'
        link = urlunsplit((
            frontend_url.scheme, frontend_url.netloc, path,
            urlencode({'token': token_str}), ''))

        return link, frontend_url.netloc

    def _create_message(self, template: str, **kwargs):
        path = Path(__file__).parent.parent / 'templates'
        environment = Environment(loader=FileSystemLoader(path))
        template = environment.get_template(template)
        return template.render(**kwargs)
