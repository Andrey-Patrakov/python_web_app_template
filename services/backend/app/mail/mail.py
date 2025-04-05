from app.config import settings

from smtplib import SMTP_SSL, SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailMessage:

    def __init__(
            self,
            session: SMTP | SMTP_SSL,
            addr_from: str,
            addr_to: str,
            subject: str):

        self._session = session
        self._from_addr = addr_from
        self._to_addr = addr_to

        self.message = MIMEMultipart()
        self.message['From'] = addr_from
        self.message['To'] = addr_to
        self.message['Subject'] = subject

    def attach(self, mime):
        self.message.attach(mime)

    def attach_text(self, text):
        self.message.attach(MIMEText(text, 'plain', 'utf-8'))

    def attach_html(self, html):
        self.message.attach(MIMEText(html, 'html', 'utf-8'))

    def send(self):
        self._session.sendmail(
            from_addr=self._from_addr,
            to_addrs=self._to_addr,
            msg=self.message.as_string())


class SMTP_Mail:

    def __init__(self):
        self._user = settings.smtp.USER
        self._password = settings.smtp.PASSWORD

        if settings.smtp.SSL_REQUIRED:
            self._session = SMTP_SSL(
                host=settings.smtp.HOST, port=settings.smtp.PORT)
        else:
            self._session = SMTP(
                host=settings.smtp.HOST, port=settings.smtp.PORT)

        self._session.login(self._user, self._password)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_val, trace):
        self.quit()

    def message(
            self,
            addr_to: str | list[str],
            subject: str) -> MailMessage:

        return MailMessage(
            self._session, self._user, addr_to, subject)

    def quit(self):
        self._session.quit()
