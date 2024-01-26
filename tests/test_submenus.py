from httpx import AsyncClient

menu_id = ''
submenu_id = ''


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


async def test_get_empty_list_submenus(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus")

    assert len(response.json()) == 0
    assert response.status_code == 200


async def test_create_submenu(ac: AsyncClient):
    global submenu_id
    response = await ac.post(f"/api/v1/menus/{menu_id}/submenus", json={
        "title": "My submenu 1",
        "description": "My submenu description 1"
    })

    json_response = response.json()

    assert response.status_code == 201
    assert "id" in json_response
    assert json_response["title"] == "My submenu 1"
    assert json_response["description"] == "My submenu description 1"
    submenu_id = json_response["id"]


async def test_get_list_submenus(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus")

    assert len(response.json()) > 0
    assert response.status_code == 200


async def test_get_submenu_by_id(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    json_response = response.json()

    assert response.status_code == 200
    assert "id" in json_response
    assert json_response["title"] == "My submenu 1"
    assert json_response["description"] == "My submenu description 1"


async def test_update_submenu(ac: AsyncClient):
    response = await ac.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}", json={
        "title": "My updated submenu 1",
        "description": "My updated submenu description 1"
    })

    json_response = response.json()

    assert response.status_code == 200
    assert "id" in json_response
    assert json_response["title"] == "My updated submenu 1"
    assert json_response["description"] == "My updated submenu description 1"


async def test_get_submenu_by_id_after_update(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")

    json_response = response.json()

    assert response.status_code == 200
    assert "id" in json_response
    assert json_response["title"] == "My updated submenu 1"
    assert json_response["description"] == "My updated submenu description 1"


async def test_delete_submenu(ac: AsyncClient):
    response = await ac.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")

    assert response.status_code == 200


async def test_get_list_submenus_after_delete(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus")

    assert len(response.json()) == 0
    assert response.status_code == 200


async def test_get_submenu_by_id_after_delete(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")

    json_response = response.json()

    assert response.status_code == 404
    assert json_response == {
        "detail": "submenu not found"
    }


async def test_delete_menu(ac: AsyncClient):
    response = await ac.delete(f"/api/v1/menus/{menu_id}")

    assert response.status_code == 200


async def test_get_list_menus(ac: AsyncClient):
    response = await ac.get("/api/v1/menus/")

    assert len(response.json()) == 0
    assert response.status_code == 200
