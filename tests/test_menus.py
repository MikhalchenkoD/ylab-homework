from httpx import AsyncClient
from sqlalchemy import select

from .conftest import TestingSessionLocal
from database.models import Menu


async def test_create_menu(ac: AsyncClient):
    data = {
        "title": "My menu 1",
        "description": "My menu description 1"
    }
    response = await ac.post("/api/v1/menus/", json=data)

    json_response = response.json()

    assert response.status_code == 201
    assert "id" in json_response
    assert json_response["title"] == data["title"]
    assert json_response["description"] == data["description"]

    async with TestingSessionLocal() as session:
        res = await session.execute(select(Menu).where(Menu.id == json_response['id']))
        menu = res.scalars().one_or_none()

        assert menu is not None
        assert menu.title == data['title']
        assert menu.description == data['description']

        await session.delete(menu)
        await session.commit()


async def test_get_list_menus(ac: AsyncClient, menu):
    response = await ac.get("/api/v1/menus/")

    assert len(response.json()) > 0
    assert response.status_code == 200


async def test_get_menu_by_id(ac: AsyncClient, menu):
    response = await ac.get(f"/api/v1/menus/{menu.id}")
    json_response = response.json()

    assert response.status_code == 200
    assert "id" in json_response
    assert json_response["title"] == menu.title
    assert json_response["description"] == menu.description


async def test_update_menu(ac: AsyncClient, menu):
    data = {
        "title": "My updated menu 1",
        "description": "My updated menu description 1"
    }

    response = await ac.patch(f"/api/v1/menus/{menu.id}", json=data)

    json_response = response.json()

    assert response.status_code == 200
    assert "id" in json_response
    assert json_response["title"] == "My updated menu 1"
    assert json_response["description"] == "My updated menu description 1"

    async with TestingSessionLocal() as session:
        res = await session.execute(select(Menu).where(Menu.id == json_response['id']))
        updated_menu = res.scalars().one_or_none()

        assert updated_menu.title == data['title']
        assert updated_menu.description == data['description']


async def test_delete_menu(ac: AsyncClient, menu):
    response = await ac.delete(f"/api/v1/menus/{menu.id}")

    assert response.status_code == 200

    async with TestingSessionLocal() as session:
        res = await session.execute(select(Menu).where(Menu.id == menu.id))
        deleted_menu = res.scalars().one_or_none()

        assert deleted_menu is None

