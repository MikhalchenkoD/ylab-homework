# Y_LAB Homework

Проект на FastAPI с использованием PostgreSQL в качестве БД. В проекте реализовано REST API по работе с меню ресторана, все CRUD операции.
Пункт №5 задания находится в repositoires/google_sheets_repository.py, parsers/google_sheets_parser.py, services/task_service.py, celery_conf.py
### Зависимости:
```
У меню есть подменю, которые к ней привязаны.
У подменю есть блюда.
```
### Условия:
```
Блюдо не может быть привязано напрямую к меню, минуя подменю.
Блюдо не может находиться в 2-х подменю одновременно.
Подменю не может находиться в 2-х меню одновременно.
Если удалить меню, должны удалиться все подменю и блюда этого меню.
Если удалить подменю, должны удалиться все блюда этого подменю.
Цены блюд выводить с округлением до 2 знаков после запятой.
Во время выдачи списка меню, для каждого меню добавлять кол-во подменю и блюд в этом меню.
Во время выдачи списка подменю, для каждого подменю добавлять кол-во блюд в этом подменю.
Во время запуска тестового сценария БД должна быть пуста.
```
## Установка и запуск

Убедитесь, что у вас установлены Docker и docker-compose.

1. Копирование репозитория:

    ```bash
    git clone https://github.com/MikhalchenkoD/ylab-homework.git
    cd ylab-homework
    ```

2. Сборка и запуск основного контейнера(убедитесь, что у вас установлен docker):

   ```bash
    docker-compose -f docker-compose-main.yaml build
    ```
      ```bash
    docker-compose -f docker-compose-main.yaml up
    ```

    Завершение работы контейнера(cntrl + c может не сработать):
   ```bash
   docker-compose -f docker-compose-main.yaml stop
   ```
3. Сборка и запуск контейнера с тестами(убедитесь, что у вас установлен docker):

   ```bash
    docker-compose -f docker-compose-test.yaml build
    ```
      ```bash
    docker-compose -f docker-compose-test.yaml up
    ```

    Завершение работы контейнера(cntrl + c может не сработать):
   ```bash
   docker-compose -f docker-compose-test.yaml stop
   ```

## Edpoints
### 1. GET Просмотр списка меню
```
127.0.0.1:8000/api/v1/menus
```

Response
```
[
    {
        "id": "a2eb416c-2245-4526-bb4b-6343d5c5016f",
        "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": 0,
        "dishes_count": 0
    }
]
```

### 2. GET Просмотр определенного меню
```
127.0.0.1:8000/api/v1/menus/{menu_id}
```

Response
```
{
    "id": "a2eb416c-2245-4526-bb4b-6343d5c5016f",
    "title": "My menu 1",
    "description": "My menu description 1",
    "submenus_count": 0,
    "dishes_count": 0
}
```

### 3. POST Создать меню
```
127.0.0.1:8000/api/v1/menus
```

Body
```
{
    "title": "My menu 1",
    "description": "My menu description 1"
}
```

Response
```
{
    "id": "9a5bce5f-4462-4d12-a66c-d59584b19ee8",
    "title": "My menu 1",
    "description": "My menu description 1",
    "submenus_count": 0,
    "dishes_count": 0
}
```

### 4. PATCH Обновить меню
```
127.0.0.1:8000/api/v1/menus/{menu_id}
```

Body
```
{
    "title": "My updated menu 1",
    "description": "My updated menu description 1"
}
```

Response
```
{
    "id": "a2eb416c-2245-4526-bb4b-6343d5c5016f",
    "title": "My updated menu 1",
    "description": "My updated menu description 1",
    "submenus_count": 0,
    "dishes_count": 0
}
```

### 5. DELETE Удалить меню
```
127.0.0.1:8000/api/v1/menus/{menu_id}
```

Response
```
{
    "status": true,
    "message": "The menu has been deleted"
}
```

### 6. GET Просмотр списка меню
```
127.0.0.1:8000/api/v1/menus/{menu_id}/submenus
```

Response
```
[
    {
        "id": "bc19488a-cc0e-4eaa-8d21-4d486a45392f",
        "title": "My submenu 1",
        "description": "My submenu description 1",
        "dishes_count": 0
    }
]
```

### 7. GET Просмотр определенного подменю
```
127.0.0.1:8000/api/v1/menus/{menu_id}/submenus/{submenu_id}
```

Response
```
{
    "id": "bc19488a-cc0e-4eaa-8d21-4d486a45392f",
    "title": "My submenu 1",
    "description": "My submenu description 1",
    "dishes_count": 0
}
```

### 8. POST Создать подменю
```
127.0.0.1:8000/api/v1/menus/{menu_id}/submenus
```

Body
```
{
    "title": "My submenu 1",
    "description": "My submenu description 1"
}
```

Response
```
{
    "id": "bc19488a-cc0e-4eaa-8d21-4d486a45392f",
    "title": "My submenu 1",
    "description": "My submenu description 1",
    "dishes_count": 0
}
```

### 9. PATCH Обновить подменю
```
127.0.0.1:8000/api/v1/menus/{menu_id}/submenus/{submenu_id}
```

Body
```
{
    "title": "My updated submenu 1",
    "description": "My updated submenu description 1"
}
```

Response
```
{
    "id": "bc19488a-cc0e-4eaa-8d21-4d486a45392f",
    "title": "My updated submenu 1",
    "description": "My updated submenu description 1",
    "dishes_count": 0
}
```

### 10. DELETE Удалить меню
```
127.0.0.1:8000/api/v1/menus/{menu_id}/submenus/{submenu_id}
```

Response
```
{
    "status": true,
    "message": "The submenu has been deleted"
}
```

### 11. GET Просмотр списка блюд
```
127.0.0.1:8000/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes
```

Response
```
[
    {
        "id": "602033b3-0462-4de1-a2f8-d8494795e0c0",
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    }
]
```

### 12. GET Просмотр определенного блюда
```
127.0.0.1:8000/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}
```

Response
```
{
    "id": "602033b3-0462-4de1-a2f8-d8494795e0c0",
    "title": "My dish 1",
    "description": "My dish description 1",
    "price": "12.50"
}
```

### 13. POST Создать блюдо
```
127.0.0.1:8000/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes
```

Body
```
{
    "title": "My dish 1",
    "description": "My dish description 1",
    "price": "12.50"
}
```

Response
```
{
    "id": "602033b3-0462-4de1-a2f8-d8494795e0c0",
    "title": "My dish 1",
    "description": "My dish description 1",
    "price": "12.50"
}
```

### 14. PATCH Обновить блюдо
```
127.0.0.1:8000/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}
```

Body
```
{
    "title": "My updated dish 1",
    "description": "My updated dish description 1",
    "price": "14.50"
}
```

Response
```
{
    "id": "602033b3-0462-4de1-a2f8-d8494795e0c0",
    "title": "My updated dish 1",
    "description": "My updated dish description 1",
    "price": "14.50"
}
```

### 15. DELETE Удалить блюдо
```
127.0.0.1:8000/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}
```

Response
```
{
    "status": true,
    "message": "The dish has been deleted"
}
```

## Авторы

Михальченко Дмитрий (https://t.me/DmitriyMikhalchenko)
