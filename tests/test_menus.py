from httpx import AsyncClient
from sqlalchemy import select

from .conftest import TestingSessionLocal, reverse
from database.models import Menu


async def test_get_empty_list_menus(ac: AsyncClient):
    url = await reverse('get_list_menus')
    response = await ac.get(url)

    assert response.status_code == 200
    assert len(response.json()) == 0


async def test_create_menu(ac: AsyncClient, buffer_data):
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


async def test_get_list_menus(ac: AsyncClient):
    url = await reverse('get_list_menus')
    response = await ac.get(url)

    assert len(response.json()) > 0
    assert response.status_code == 200


async def test_get_menu_by_id(ac: AsyncClient, buffer_data):
    url = await reverse('get_menu_by_id', menu_id=buffer_data['menu']['id'])
    response = await ac.get(url)
    json_response = response.json()

    assert response.status_code == 200
    assert 'id' in json_response
    assert json_response['title'] == buffer_data['menu']['title']
    assert json_response['description'] == buffer_data['menu']['description']


async def test_update_menu(ac: AsyncClient, buffer_data):
    data = {
        'title': 'My updated menu 1',
        'description': 'My updated menu description 1'
    }
    url = await reverse('update_menu_by_id', menu_id=buffer_data['menu']['id'])
    response = await ac.patch(url, json=data)

    json_response = response.json()
    buffer_data['menu'] = json_response

    assert response.status_code == 200
    assert 'id' in json_response
    assert json_response['title'] == data['title']
    assert json_response['description'] == data['description']

    async with TestingSessionLocal() as session:
        res = await session.execute(select(Menu).where(Menu.id == json_response['id']))
        updated_menu = res.scalars().one_or_none()

        assert updated_menu.title == data['title']
        assert updated_menu.description == data['description']


async def test_get_menu_by_id_after_update(ac: AsyncClient, buffer_data):
    url = await reverse('get_menu_by_id', menu_id=buffer_data['menu']['id'])
    response = await ac.get(url)
    json_response = response.json()

    assert response.status_code == 200
    assert 'id' in json_response
    assert json_response['title'] == buffer_data['menu']['title']
    assert json_response['description'] == buffer_data['menu']['description']


async def test_delete_menu(ac: AsyncClient, buffer_data):
    url = await reverse('delete_menu_by_id', menu_id=buffer_data['menu']['id'])
    response = await ac.delete(url)

    assert response.status_code == 200

    async with TestingSessionLocal() as session:
        res = await session.execute(select(Menu).where(Menu.id == buffer_data['menu']['id']))
        deleted_menu = res.scalars().one_or_none()

        assert deleted_menu is None


async def test_get_list_menus_after_delete(ac: AsyncClient):
    url = await reverse('get_list_menus')
    response = await ac.get(url)

    assert response.status_code == 200
    assert len(response.json()) == 0


async def test_get_menu_by_id_after_delete(ac: AsyncClient, buffer_data):
    url = await reverse('get_menu_by_id', menu_id=buffer_data['menu']['id'])
    response = await ac.get(url)

    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}

    buffer_data.clear()
