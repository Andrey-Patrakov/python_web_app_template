from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.storage import Storage
from app.user.token import Token


async def on_every_hour():
    await Token.clear_dead_tokens()


def on_start(app):
    storage = Storage()
    storage.make_bucket(storage.bucket)


def on_finish(app):
    pass


@asynccontextmanager
async def lifespan(app):
    on_start(app)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        on_every_hour,
        trigger=IntervalTrigger(hours=1),
        id='on_every_hour',
        replace_existing=True)
    scheduler.start()

    yield
    on_finish(app)
    scheduler.shutdown()
