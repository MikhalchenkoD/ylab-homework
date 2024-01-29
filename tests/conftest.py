import asyncio
import uuid
from decimal import Decimal
from typing import AsyncGenerator
import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from database.models import Base, Menu, Submenu, Dish
from database.database import get_async_session
from main import app

DATABASE_URL_TEST = "postgresql+asyncpg://postgres:admin@postgres_tests_ylab/ylabtest"
engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
TestingSessionLocal = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)


async def override_get_async_session():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database(request):
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)





@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def menu():
    async with TestingSessionLocal() as session:
        new_menu = Menu(id=uuid.uuid4(), title='test title', description='test description')

        session.add(new_menu)
        await session.commit()

        yield new_menu

        res = await session.execute(select(Menu).where(Menu.id == new_menu.id))
        result = res.scalars().one_or_none()
        if result:
            await session.delete(new_menu)
            await session.commit()

@pytest.fixture(scope="function")
async def submenu(menu):
    async with TestingSessionLocal() as session:
        new_submenu = Submenu(id=uuid.uuid4(), title='test title', description='test description', menu_id=menu.id)

        session.add(new_submenu)
        await session.commit()

        yield new_submenu

        res = await session.execute(select(Submenu).where(Submenu.id == new_submenu.id))
        result = res.scalars().one_or_none()
        if result:
            await session.delete(new_submenu)
            await session.commit()


@pytest.fixture(scope="function")
async def first_dish(submenu):
    async with TestingSessionLocal() as session:

        new_dish = Dish(id=uuid.uuid4(), title='test title 1', description='test description 1', price='12.50',
                        submenu_id=submenu.id)

        session.add(new_dish)
        await session.commit()

        yield new_dish

        res = await session.execute(select(Dish).where(Dish.id == new_dish.id))
        result = res.scalars().one_or_none()
        if result:
            await session.delete(new_dish)
            await session.commit()

@pytest.fixture(scope="function")
async def second_dish(submenu):
    async with TestingSessionLocal() as session:
        new_dish = Dish(id=uuid.uuid4(), title='test title 2', description='test description 2', price='12.50',
                        submenu_id=submenu.id)

        session.add(new_dish)
        await session.commit()

        yield new_dish

        res = await session.execute(select(Dish).where(Dish.id == new_dish.id))
        result = res.scalars().one_or_none()
        if result:
            await session.delete(new_dish)
            await session.commit()
