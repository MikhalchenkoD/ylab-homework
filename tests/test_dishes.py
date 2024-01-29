from sqlalchemy import select

from httpx import AsyncClient

from database.models import Dish, Menu, Submenu
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


async def test_get_empty_list_dishes(ac: AsyncClient, buffer_data):
    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}/dishes")

    assert response.status_code == 200
    assert len(response.json()) == 0


async def test_create_dish(ac: AsyncClient, buffer_data):
    data = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": '12.50'
    }
    response = await ac.post(
        f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}/dishes", json=data)

    json_response = response.json()
    buffer_data.update(dish=json_response)

    assert response.status_code == 201
    assert "id" in json_response
    assert json_response["title"] == data['title']
    assert json_response["description"] == data['description']
    assert json_response["price"] == data['price']

    async with TestingSessionLocal() as session:
        res = await session.execute(select(Dish).where(Dish.id == json_response['id']))
        dish = res.scalars().one_or_none()

        assert dish is not None
        assert dish.title == data['title']
        assert dish.description == data['description']
        assert dish.price == data['price']


async def test_get_list_dishes(ac: AsyncClient, buffer_data):
    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}/dishes")

    assert len(response.json()) > 0
    assert response.status_code == 200


async def test_get_dish_by_id(ac: AsyncClient, buffer_data):
    response = await ac.get(
        f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}/dishes/{buffer_data['dish']['id']}")
    json_response = response.json()

    assert response.status_code == 200
    assert "id" in json_response
    assert json_response["title"] == buffer_data['dish']['title']
    assert json_response["description"] == buffer_data['dish']['description']
    assert json_response["price"] == buffer_data['dish']['price']


async def test_update_dish(ac: AsyncClient, buffer_data):
    data = {
        "title": "My updated dish 1",
        "description": "My updated dish description 1",
        "price": '14.50'
    }
    response = await ac.patch(
        f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}/dishes/{buffer_data['dish']['id']}",
        json=data)

    json_response = response.json()
    buffer_data.update(dish=json_response)

    assert response.status_code == 200
    assert "id" in json_response
    assert json_response["title"] == data['title']
    assert json_response["description"] == data['description']
    assert json_response["price"] == data['price']

    async with TestingSessionLocal() as session:
        res = await session.execute(select(Dish).where(Dish.id == json_response['id']))
        dish = res.scalars().one_or_none()

        assert dish is not None
        assert dish.title == data['title']
        assert dish.description == data['description']
        assert dish.price == data['price']


async def test_get_dish_by_id_after_update(ac: AsyncClient, buffer_data):
    response = await ac.get(
        f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}/dishes/{buffer_data['dish']['id']}")
    json_response = response.json()

    assert response.status_code == 200
    assert "id" in json_response
    assert json_response["title"] == buffer_data['dish']['title']
    assert json_response["description"] == buffer_data['dish']['description']
    assert json_response["price"] == buffer_data['dish']['price']


async def test_delete_dish(ac: AsyncClient, buffer_data):
    response = await ac.delete(
        f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}/dishes/{buffer_data['dish']['id']}")

    assert response.status_code == 200

    async with TestingSessionLocal() as session:
        res = await session.execute(select(Dish).where(Dish.id == buffer_data['dish']['id']))
        dish = res.scalars().one_or_none()

        assert dish is None


async def test_get_list_dishes_after_delete(ac: AsyncClient, buffer_data):
    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}/dishes")

    assert len(response.json()) == 0
    assert response.status_code == 200


async def test_get_dish_by_id_after_delete(ac: AsyncClient, buffer_data):
    response = await ac.get(
        f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}/dishes/{buffer_data['dish']['id']}")
    json_response = response.json()

    assert response.status_code == 404
    assert json_response == {"detail": "dish not found"}


async def test_delete_submenu(ac: AsyncClient, buffer_data):
    response = await ac.delete(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus/{buffer_data['submenu']['id']}")

    assert response.status_code == 200

    async with TestingSessionLocal() as session:
        res = await session.execute(select(Submenu).where(Submenu.id == buffer_data['submenu']['id']))
        deleted_submenu = res.scalars().one_or_none()

        assert deleted_submenu is None


async def test_get_list_submenus_after_delete(ac: AsyncClient, buffer_data):
    response = await ac.get(f"/api/v1/menus/{buffer_data['menu']['id']}/submenus")

    assert response.status_code == 200
    assert len(response.json()) == 0


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