from typing import List, Union

from pydantic import (
    BaseModel,
    field_validator,
    computed_field,
    UUID4,
    Field,
)


class DishIn(BaseModel):
    title: str
    description: str
    price: str


class DishOut(DishIn):
    id: UUID4

    @field_validator("price")
    def round_price(cls, v: str):
        v = float(v)
        return str("{:.2f}".format(v))


class SubmenuIn(BaseModel):
    title: str
    description: str


class SubmenuOut(SubmenuIn):
    id: UUID4
    dishes_count: int


class MenuIn(BaseModel):
    title: str
    description: str


class MenuOut(MenuIn):
    id: UUID4
    submenus_count: int
    dishes_count: int
