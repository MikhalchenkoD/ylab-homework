from httpx import AsyncClient

menu_id = ''
submenu_id = ''
dishes_id_first = ''
dishes_id_second = ''


async def test_create_menu(ac: AsyncClient):
    global menu_id
    response = await ac.post("/api/v1/menus/", json={
        "title": "My menu 1",
        "description": "My menu description 1"
    })

    json_response = response.json()

    assert response.status_code == 201
    assert "id" in json_response

    menu_id = json_response["id"]


async def test_create_submenu(ac: AsyncClient):
    global submenu_id
    response = await ac.post(f"/api/v1/menus/{menu_id}/submenus", json={
        "title": "My submenu 1",
        "description": "My submenu description 1"
    })

    json_response = response.json()

    assert response.status_code == 201
    assert "id" in json_response

    submenu_id = json_response["id"]


async def test_create_first_dish(ac: AsyncClient):
    global dishes_id_first
    response = await ac.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json={
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    })

    json_response = response.json()

    assert response.status_code == 201
    assert "id" in json_response

    dishes_id_first = json_response["id"]


async def test_create_second_dish(ac: AsyncClient):
    global dishes_id_second
    response = await ac.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json={
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    })

    json_response = response.json()

    assert response.status_code == 201
    assert "id" in json_response

    dishes_id_second = json_response["id"]


async def test_get_menu_by_id(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}")
    json_response = response.json()

    assert response.status_code == 200
    assert "id" in json_response
    assert json_response['submenus_count'] == 1
    assert json_response['dishes_count'] == 2


async def test_get_submenu_by_id(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    json_response = response.json()

    assert response.status_code == 200
    assert "id" in json_response
    assert json_response['dishes_count'] == 2


async def test_delete_submenu(ac: AsyncClient):
    response = await ac.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")

    json_response = response.json()

    assert response.status_code == 200


async def test_get_list_submenus_after_delete(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus")

    assert len(response.json()) == 0
    assert response.status_code == 200


async def test_get_list_dishes_after_delete_submenu(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")

    assert len(response.json()) == 0
    assert response.status_code == 200


async def test_get_menu_by_id_after_delete_submenu(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}")
    json_response = response.json()

    assert response.status_code == 200
    assert "id" in json_response
    assert json_response['submenus_count'] == 0
    assert json_response['dishes_count'] == 0


async def test_delete_menu(ac: AsyncClient):
    response = await ac.delete(f"/api/v1/menus/{menu_id}")

    json_response = response.json()

    assert response.status_code == 200


async def test_get_list_menus_after_delete(ac: AsyncClient):
    response = await ac.get("/api/v1/menus/")

    assert len(response.json()) == 0
    assert response.status_code == 200
