from httpx import AsyncClient
from sqlalchemy import select

from database.models import Submenu
from .conftest import TestingSessionLocal


async def test_create_submenu(ac: AsyncClient, menu):
    data = {
        "title": "My submenu 1",
        "description": "My submenu description 1"
    }
    response = await ac.post(f"/api/v1/menus/{menu.id}/submenus", json=data)

    json_response = response.json()

    assert response.status_code == 201
    assert "id" in json_response
    assert json_response["title"] == data['title']
    assert json_response["description"] == data['description']

    async with TestingSessionLocal() as session:
        res = await session.execute(select(Submenu).where(Submenu.id == json_response['id']))
        submenu = res.scalars().one_or_none()

        assert submenu is not None
        assert submenu.title == data['title']
        assert submenu.description == data['description']

        await session.delete(submenu)
        await session.commit()


async def test_get_list_submenus(ac: AsyncClient, menu, submenu):
    response = await ac.get(f"/api/v1/menus/{menu.id}/submenus")

    assert len(response.json()) > 0
    assert response.status_code == 200


async def test_get_submenu_by_id(ac: AsyncClient, menu, submenu):
    response = await ac.get(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}")
    json_response = response.json()

    assert response.status_code == 200
    assert "id" in json_response
    assert json_response["title"] == menu.title
    assert json_response["description"] == menu.description


async def test_update_submenu(ac: AsyncClient, menu, submenu):
    data = {
        "title": "My updated submenu 1",
        "description": "My updated submenu description 1"
    }
    response = await ac.patch(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}", json=data)

    json_response = response.json()

    assert response.status_code == 200
    assert "id" in json_response
    assert json_response["title"] == data['title']
    assert json_response["description"] == data['description']

    async with TestingSessionLocal() as session:
        res = await session.execute(select(Submenu).where(Submenu.id == json_response['id']))
        updated_submenu = res.scalars().one_or_none()

        assert updated_submenu.title == data['title']
        assert updated_submenu.description == data['description']


async def test_delete_submenu(ac: AsyncClient, menu, submenu):
    response = await ac.delete(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}")

    assert response.status_code == 200

    async with TestingSessionLocal() as session:
        res = await session.execute(select(Submenu).where(Submenu.id == submenu.id))
        deleted_submenu = res.scalars().one_or_none()

        assert deleted_submenu is None


