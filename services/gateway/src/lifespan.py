from contextlib import asynccontextmanager
from services.storage.utils import make_bucket
from src.config import settings


def on_start(app):
    make_bucket(settings.storage.BUCKET)


def on_finish(app):
    pass


@asynccontextmanager
async def lifespan(app):
    on_start(app)
    yield
    on_finish(app)
