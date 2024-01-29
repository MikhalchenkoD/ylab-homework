from httpx import AsyncClient



async def test_get_menu_by_id(ac: AsyncClient, menu, submenu, first_dish, second_dish):
    response = await ac.get(f"/api/v1/menus/{menu.id}")
    json_response = response.json()

    assert response.status_code == 200
    assert "id" in json_response
    assert json_response['submenus_count'] == 1
    assert json_response['dishes_count'] == 2


async def test_get_submenu_by_id(ac: AsyncClient, menu, submenu, first_dish, second_dish):
    response = await ac.get(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}")
    json_response = response.json()

    assert response.status_code == 200
    assert "id" in json_response
    assert json_response['dishes_count'] == 2


async def test_get_list_dishes_after_delete_submenu(ac: AsyncClient, menu, submenu, first_dish, second_dish):
    await ac.delete(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}")
    response = await ac.get(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes")

    assert len(response.json()) == 0
    assert response.status_code == 200


async def test_get_menu_by_id_after_delete_submenu(ac: AsyncClient, menu, submenu, first_dish, second_dish):
    await ac.delete(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}")
    response = await ac.get(f"/api/v1/menus/{menu.id}")
    json_response = response.json()

    assert response.status_code == 200
    assert "id" in json_response
    assert json_response['submenus_count'] == 0
    assert json_response['dishes_count'] == 0


