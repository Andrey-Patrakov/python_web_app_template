from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from storage import Storage
from src.services.tokens import TokenService


async def on_every_hour():
    token_service = TokenService()
    await token_service.clear_dead()


def on_start(app):
    Storage().make_bucket()


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
