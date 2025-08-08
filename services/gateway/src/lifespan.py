from contextlib import asynccontextmanager
from storage import Storage


def on_start(app):
    Storage().make_bucket()


def on_finish(app):
    pass


@asynccontextmanager
async def lifespan(app):
    on_start(app)
    yield
    on_finish(app)
