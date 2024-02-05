import uvicorn
from fastapi import FastAPI

from config import BASE_API_URL
from routes.routes_for_dish import dishes_router
from routes.routes_for_menu import menus_router
from routes.routes_for_submenu import submenus_router

app = FastAPI()

app.include_router(menus_router, prefix=f'{BASE_API_URL}')
app.include_router(submenus_router, prefix=f'{BASE_API_URL}')
app.include_router(dishes_router, prefix=f'{BASE_API_URL}')

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
