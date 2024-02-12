from pydantic import UUID4, BaseModel, ValidationError, field_validator


class DishIn(BaseModel):
    title: str
    description: str
    price: str


class DishOut(DishIn):
    id: UUID4

    @field_validator('price')
    def round_price(cls, v: str) -> str:
        try:
            price_float = float(v)
        except ValueError:
            raise ValidationError('Invalid price format')

        return str(f'{price_float:.2f}')


class SubmenuIn(BaseModel):
    title: str
    description: str


class Submenu(SubmenuIn):
    id: UUID4


class SubmenuOut(Submenu):
    dishes_count: int


class MenuIn(BaseModel):
    title: str
    description: str


class Menu(MenuIn):
    id: UUID4


class MenuOut(Menu):
    submenus_count: int
    dishes_count: int


class MenuOutWithSubmenusAndDishes(Menu):
    submenus: list[SubmenuOut]
    dishes: list[DishOut]


class OutAfterDelete(BaseModel):
    status: bool
    message: str


class NotFoundError(BaseModel):
    detail: str
