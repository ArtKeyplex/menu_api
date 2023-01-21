from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import models, schemas


def count_submenus(db: Session, id: str):
    parent = db.query(models.Menu).filter(models.Menu.id == id).first()
    return len(parent.submenus)


def count_dishes(db: Session, id: str):
    return db.query(
        models.Dish).join(models.SubMenu,
                          models.Dish.parent_id == models.SubMenu.id
                          ).join(models.Menu,
                                 models.Menu.id == models.SubMenu.parent_id
                                 ).filter(models.Menu.id == id).count()


def dishes_for_submenu(db: Session, id: str):
    parent = db.query(models.SubMenu).filter(models.SubMenu.id == id).first()
    return len(parent.dishes)


def get_menus(db: Session):
    return db.query(models.Menu).all()


def get_one_menu(db: Session, id: str):
    menu = db.query(models.Menu).filter(models.Menu.id == id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return menu


def create_menu(db: Session, menu: schemas.MenuCreate):
    db_item = models.Menu(**menu.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_menu(db: Session, id: str, menu: schemas.MenuBase):
    one_menu = get_one_menu(db, id)
    if not one_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    menu_data = menu.dict(exclude_unset=True)
    for key, value in menu_data.items():
        setattr(one_menu, key, value)
    db.add(one_menu)
    db.commit()
    db.refresh(one_menu)
    return one_menu


def delete_menu(db: Session, id: str):
    one_menu = get_one_menu(db, id)
    if not one_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    db.delete(one_menu)
    db.commit()
    return {'status': 'true', 'message': 'The menu has been deleted'}


def get_submenus(db: Session):
    return db.query(models.SubMenu).all()


def get_one_submenu(db: Session, id: str):
    one_submenu = db.query(models.SubMenu).filter(
        models.SubMenu.id == id).first()
    if not one_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    return one_submenu


def create_submenu(db: Session, submenu: schemas.SubMenuCreate,
                   parent_id: str):
    db_item = models.SubMenu(**submenu.dict(), parent_id=parent_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_submenu(db: Session, submenu: schemas.SubmenuBase, id: str):
    one_submenu = get_one_submenu(db=db, id=id)
    if not one_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    submenu_data = submenu.dict(exclude_unset=True)
    for key, value in submenu_data.items():
        setattr(one_submenu, key, value)
    db.add(one_submenu)
    db.commit()
    db.refresh(one_submenu)
    return one_submenu


def delete_submenu(db: Session, id: str):
    one_submenu = get_one_submenu(db, id)
    if not one_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    db.delete(one_submenu)
    db.commit()
    return {'status': 'true', 'message': 'The submenu has been deleted'}


def get_dishes(db: Session):
    return db.query(models.Dish).all()


def get_one_dish(db: Session, id: str):
    dish = db.query(models.Dish).filter(models.Dish.id == id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")
    return dish


def create_dish(db: Session, dish: schemas.DishCreate, parent_id: str):
    db_item = models.Dish(**dish.dict(), parent_id=parent_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_dish(db: Session, dish: schemas.DishBase, id: str):
    one_dish = get_one_dish(db=db, id=id)
    if not one_dish:
        raise HTTPException(status_code=404, detail="dish not found")
    submenu_data = dish.dict(exclude_unset=True)
    for key, value in submenu_data.items():
        setattr(one_dish, key, value)
    db.add(one_dish)
    db.commit()
    db.refresh(one_dish)
    return one_dish


def delete_dish(db: Session, id: str):
    one_dish = get_one_dish(db, id)
    if not one_dish:
        raise HTTPException(status_code=404, detail="dish not found")
    db.delete(one_dish)
    db.commit()
    return {'status': 'true', 'message': 'The dish has been deleted'}
