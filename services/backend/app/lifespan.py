from contextlib import asynccontextmanager
from app.storage import Storage


def on_start(app):
    storage = Storage()
    storage.make_bucket(storage.bucket)


def on_finish(app):
    pass


@asynccontextmanager
async def lifespan(app):
    on_start(app)
    yield
    on_finish(app)
