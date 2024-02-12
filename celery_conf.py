import asyncio

from celery import Celery

from database.database import async_session
from services.task_service import TaskService

celery_app = Celery(
    'tasks',
    broker='pyamqp://admin:admin@rabbitmq_ylab:5672',
    backend='rpc://',
)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(15, check_google_sheets.s())


@celery_app.task
def check_google_sheets():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(check_google_sheets_async())
    return result


async def check_google_sheets_async():
    async with async_session() as session:
        return await TaskService(session).check_data()
