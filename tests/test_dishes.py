from sqlalchemy import select

from httpx import AsyncClient

from database.models import Dish
from .conftest import TestingSessionLocal


async def test_create_dish(ac: AsyncClient, menu, submenu):
    data = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": '12.50'
    }
    response = await ac.post(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes", json=data)

    json_response = response.json()

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

        await session.delete(dish)
        await session.commit()


async def test_get_list_dishes(ac: AsyncClient, menu, submenu, first_dish):
    response = await ac.get(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes")

    assert len(response.json()) > 0
    assert response.status_code == 200


async def test_get_dish_by_id(ac: AsyncClient, menu, submenu, first_dish):
    response = await ac.get(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{first_dish.id}")
    json_response = response.json()

    assert response.status_code == 200
    assert "id" in json_response
    assert json_response["title"] == first_dish.title
    assert json_response["description"] == first_dish.description
    assert json_response["price"] == first_dish.price


async def test_update_dish(ac: AsyncClient, menu, submenu, first_dish):
    data = {
        "title": "My updated dish 1",
        "description": "My updated dish description 1",
        "price": '14.50'
    }
    response = await ac.patch(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{first_dish.id}", json=data)

    json_response = response.json()

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


async def test_delete_dish(ac: AsyncClient, menu, submenu, first_dish):
    response = await ac.delete(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{first_dish.id}")

    assert response.status_code == 200

    async with TestingSessionLocal() as session:
        res = await session.execute(select(Dish).where(Dish.id == first_dish.id))
        dish = res.scalars().one_or_none()

        assert dish is None