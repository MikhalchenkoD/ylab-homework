from httpx import AsyncClient
from sqlalchemy import select

from database.models import Submenu, Menu
from .conftest import TestingSessionLocal


async def test_create_menu(ac: AsyncClient, buffer_data):
    data = {
        "title": "My menu 1",
        "description": "My menu description 1"
    }
    response = await ac.post("/api/v1/menus/", json=data)

    json_response = response.json()
    buffer_data.update(menu=json_response)

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


async def test_get_empty_list_submenus(ac: AsyncClient, buffer_data):
    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus")

    assert response.status_code == 200
    assert len(response.json()) == 0


async def test_create_submenu(ac: AsyncClient, buffer_data):
    data = {
        "title": "My submenu 1",
        "description": "My submenu description 1"
    }
    response = await ac.post(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus", json=data)

    json_response = response.json()
    buffer_data.update(submenu=response.json())

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


async def test_get_list_submenus(ac: AsyncClient, buffer_data):
    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus")

    assert len(response.json()) > 0
    assert response.status_code == 200


async def test_get_submenu_by_id(ac: AsyncClient, buffer_data):
    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}")
    json_response = response.json()

    assert response.status_code == 200
    assert "id" in json_response
    assert json_response["title"] == buffer_data["submenu"]["title"]
    assert json_response["description"] == buffer_data["submenu"]["description"]


async def test_update_submenu(ac: AsyncClient, buffer_data):
    data = {
        "title": "My updated submenu 1",
        "description": "My updated submenu description 1"
    }
    response = await ac.patch(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}",
                              json=data)

    json_response = response.json()
    buffer_data["submenu"] = json_response

    assert response.status_code == 200
    assert "id" in json_response
    assert json_response["title"] == data['title']
    assert json_response["description"] == data['description']

    async with TestingSessionLocal() as session:
        res = await session.execute(select(Submenu).where(Submenu.id == json_response['id']))
        updated_submenu = res.scalars().one_or_none()

        assert updated_submenu.title == data['title']
        assert updated_submenu.description == data['description']


async def test_get_submenu_by_id_after_update(ac: AsyncClient, buffer_data):
    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}")
    json_response = response.json()

    assert response.status_code == 200
    assert "id" in json_response
    assert json_response["title"] == buffer_data["submenu"]["title"]
    assert json_response["description"] == buffer_data["submenu"]["description"]


async def test_delete_submenu(ac: AsyncClient, buffer_data):
    response = await ac.delete(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}")

    assert response.status_code == 200

    async with TestingSessionLocal() as session:
        res = await session.execute(select(Submenu).where(Submenu.id == buffer_data['submenu']['id']))
        deleted_submenu = res.scalars().one_or_none()

        assert deleted_submenu is None


async def test_get_list_submenus_after_delete(ac: AsyncClient, buffer_data):
    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus")

    assert len(response.json()) == 0
    assert response.status_code == 200


async def test_get_submenu_by_id_after_delete(ac: AsyncClient, buffer_data):

    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}")

    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}


async def test_delete_menu(ac: AsyncClient, buffer_data):
    response = await ac.delete(f"/api/v1/menus/{buffer_data['menu']['id']}")

    assert response.status_code == 200

    async with TestingSessionLocal() as session:
        res = await session.execute(select(Menu).where(Menu.id == buffer_data['menu']['id']))
        deleted_menu = res.scalars().one_or_none()

        assert deleted_menu is None


async def test_get_list_menus_after_delete(ac: AsyncClient, buffer_data):
    response = await ac.get("/api/v1/menus/")

    assert response.status_code == 200
    assert len(response.json()) == 0

    buffer_data.clear()