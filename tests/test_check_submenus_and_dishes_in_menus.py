from typing import Any

from httpx import AsyncClient
from sqlalchemy import select

from database.models import Dish, Menu, Submenu

from .conftest import TestingSessionLocal, reverse


async def test_create_menu(ac: AsyncClient, buffer_data: dict[str, Any]) -> None:
    data = {
        'title': 'My menu 1',
        'description': 'My menu description 1'
    }
    url = await reverse('create_menu')
    response = await ac.post(url, json=data)

    json_response = response.json()
    buffer_data.update(menu=json_response)

    assert response.status_code == 201
    assert 'id' in json_response
    assert json_response['title'] == data['title']
    assert json_response['description'] == data['description']

    async with TestingSessionLocal() as session:
        res = await session.execute(select(Menu).where(Menu.id == json_response['id']))
        menu = res.scalars().one_or_none()

        assert menu is not None
        assert menu.title == data['title']
        assert menu.description == data['description']


async def test_get_menus_list(ac: AsyncClient, buffer_data: dict[str, Any]) -> None:
    url = await reverse('get_list_menus_with_submenus_and_dishes')
    response = await ac.get(url)
    json_response = response.json()

    assert response.status_code == 200
    assert len(json_response[0]['submenus']) == 0


async def test_create_submenu(ac: AsyncClient, buffer_data: dict[str, Any]) -> None:
    data = {
        'title': 'My submenu 1',
        'description': 'My submenu description 1'
    }
    url = await reverse('create_submenu', menu_id=buffer_data['menu']['id'])
    response = await ac.post(url, json=data)

    json_response = response.json()
    buffer_data.update(submenu=response.json())

    assert response.status_code == 201
    assert 'id' in json_response
    assert json_response['title'] == data['title']
    assert json_response['description'] == data['description']

    async with TestingSessionLocal() as session:
        res = await session.execute(select(Submenu).where(Submenu.id == json_response['id']))
        submenu = res.scalars().one_or_none()

        assert submenu is not None
        assert submenu.title == data['title']
        assert submenu.description == data['description']


async def test_get_menus_list_after_create_submenu(ac: AsyncClient, buffer_data: dict[str, Any]) -> None:
    url = await reverse('get_list_menus_with_submenus_and_dishes')
    response = await ac.get(url)
    json_response = response.json()

    assert response.status_code == 200
    assert len(json_response[0]['submenus']) == 1
    assert len(json_response[0]['submenus'][0]['dishes']) == 0


async def test_create_first_dish(ac: AsyncClient, buffer_data: dict[str, Any]) -> None:
    data = {
        'title': 'My dish 1',
        'description': 'My dish description 1',
        'price': '12.50'
    }
    url = await reverse('create_dish', menu_id=buffer_data['menu']['id'], submenu_id=buffer_data['submenu']['id'])
    response = await ac.post(url, json=data)

    json_response = response.json()
    buffer_data.update(first_dish=json_response)

    assert response.status_code == 201
    assert 'id' in json_response
    assert json_response['title'] == data['title']
    assert json_response['description'] == data['description']
    assert json_response['price'] == data['price']

    async with TestingSessionLocal() as session:
        res = await session.execute(select(Dish).where(Dish.id == json_response['id']))
        dish = res.scalars().one_or_none()

        assert dish is not None
        assert dish.title == data['title']
        assert dish.description == data['description']
        assert dish.price == data['price']


async def test_create_second_dish(ac: AsyncClient, buffer_data: dict[str, Any]) -> None:
    data = {
        'title': 'My dish 1',
        'description': 'My dish description 1',
        'price': '12.50'
    }
    url = await reverse('create_dish', menu_id=buffer_data['menu']['id'], submenu_id=buffer_data['submenu']['id'])
    response = await ac.post(url, json=data)

    json_response = response.json()
    buffer_data.update(second_dish=json_response)

    assert response.status_code == 201
    assert 'id' in json_response
    assert json_response['title'] == data['title']
    assert json_response['description'] == data['description']
    assert json_response['price'] == data['price']

    async with TestingSessionLocal() as session:
        res = await session.execute(select(Dish).where(Dish.id == json_response['id']))
        dish = res.scalars().one_or_none()

        assert dish is not None
        assert dish.title == data['title']
        assert dish.description == data['description']
        assert dish.price == data['price']


async def test_get_menus_list_after_create_dishes(ac: AsyncClient, buffer_data: dict[str, Any]) -> None:
    url = await reverse('get_list_menus_with_submenus_and_dishes')
    response = await ac.get(url)
    json_response = response.json()

    assert response.status_code == 200
    assert len(json_response[0]['submenus']) == 1
    assert len(json_response[0]['submenus'][0]['dishes']) == 2


async def test_delete_submenu(ac: AsyncClient, buffer_data: dict[str, Any]) -> None:
    url = await reverse('delete_submenu_by_id', menu_id=buffer_data['menu']['id'],
                        submenu_id=buffer_data['submenu']['id'])
    response = await ac.delete(url)

    assert response.status_code == 200

    async with TestingSessionLocal() as session:
        res = await session.execute(select(Submenu).where(Submenu.id == buffer_data['submenu']['id']))
        deleted_submenu = res.scalars().one_or_none()

        assert deleted_submenu is None


async def test_get_menus_list_after_delete_submenu(ac: AsyncClient, buffer_data: dict[str, Any]) -> None:
    url = await reverse('get_list_menus_with_submenus_and_dishes')
    response = await ac.get(url)
    json_response = response.json()

    assert response.status_code == 200
    assert len(json_response[0]['submenus']) == 0


async def test_delete_menu(ac: AsyncClient, buffer_data: dict[str, Any]) -> None:
    url = await reverse('delete_menu_by_id', menu_id=buffer_data['menu']['id'])
    response = await ac.delete(url)

    assert response.status_code == 200

    async with TestingSessionLocal() as session:
        res = await session.execute(select(Menu).where(Menu.id == buffer_data['menu']['id']))
        deleted_menu = res.scalars().one_or_none()

        assert deleted_menu is None


async def test_get_list_menu_after_delete_menu(ac: AsyncClient, buffer_data: dict[str, Any]) -> None:
    url = await reverse('get_list_menus_with_submenus_and_dishes')
    response = await ac.get(url)

    assert response.status_code == 200
    assert len(response.json()) == 0

    buffer_data.clear()
