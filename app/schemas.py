from uuid import UUID

from pydantic import BaseModel, validator

from .database import get_db

db = get_db()


class MenuBase(BaseModel):
    title: str
    description: str | None = None


class MenuCreate(MenuBase):
    pass


class Menu(MenuBase):
    id: str | UUID
    submenus_count: int = 0
    dishes_count: int = 0

    class Config:
        orm_mode = True


class SubmenuBase(BaseModel):
    title: str
    description: str | None = None


class SubMenuCreate(SubmenuBase):
    pass


class SubMenu(SubmenuBase):
    id: str | UUID
    dishes_count: int = 0

    class Config:
        orm_mode = True


class DishBase(BaseModel):
    title: str
    description: str | None = None
    price: str


class DishCreate(DishBase):
    pass


class Dish(DishBase):
    id: str | UUID

    class Config:
        orm_mode = True

    @validator('price')
    def change_price(cls, price):
        return str(round(float(price), 2))
