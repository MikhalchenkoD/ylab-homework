from typing import AsyncGenerator, Any
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from database.models import Base
from database.database import get_async_session
from main import app

DATABASE_URL_TEST = 'postgresql+asyncpg://postgres:admin@postgres_tests_ylab/ylabtest'
engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
TestingSessionLocal = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)


async def override_get_async_session():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


async def reverse(route_name: str, **path_params):
    for route in app.routes:
        if route.name == route_name:
            url = route.path.format(**path_params)
            return url


@pytest.fixture(autouse=True, scope='session')
async def prepare_database(request):
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='session')
def buffer_data() -> dict[str, Any]:
    return {}
