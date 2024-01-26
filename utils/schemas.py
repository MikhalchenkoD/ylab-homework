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
    price: Union[float, str]

    @field_validator("price")
    def parse_price(cls, v: Union[float, str]):
        if isinstance(v, str):
            return float(v)
        return v


class DishOut(DishIn):
    id: UUID4

    @field_validator("price")
    def round_price(cls, v: float):
        return "{:.2f}".format(v)


class SubmenuIn(BaseModel):
    title: str
    description: str


class SubmenuOut(SubmenuIn):
    id: UUID4
    dishes: List[DishIn] = Field(..., exclude=True)

    @computed_field(return_type=int)
    def dishes_count(self):
        return len(self.dishes)


class MenuIn(BaseModel):
    title: str
    description: str


class MenuOut(MenuIn):
    id: UUID4
    submenus: List[SubmenuOut] = Field(..., exclude=True)

    @computed_field(return_type=int)
    def submenus_count(self):
        return len(self.submenus)

    @computed_field(return_type=int)
    def dishes_count(self):
        return sum(len(submenu.dishes) for submenu in self.submenus)
