from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import engine, get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get('/api/v1/menus', response_model=list[schemas.Menu])
def get_menus(db: Session = Depends(get_db)):
    menu = crud.get_menus(db=db)
    response = []
    for value in menu:
        response.append(
            schemas.Menu(id=value.id, title=value.title,
                         description=value.description,
                         submenus_count=crud.count_submenus(
                             db=db, id=value.id),
                         dishes_count=crud.count_dishes(db=db, id=value.id)
                         )
        )
    return response


@app.get('/api/v1/menus/{menu_id}')
def get_menu(menu_id: str, db: Session = Depends(get_db)):
    menu = crud.get_one_menu(db, id=menu_id)
    count_sub = crud.count_submenus(db=db, id=menu_id)
    count_dish = crud.count_dishes(db=db, id=menu_id)
    return schemas.Menu(id=menu.id, title=menu.title,
                        description=menu.description,
                        submenus_count=count_sub, dishes_count=count_dish)


@app.post('/api/v1/menus', response_model=schemas.Menu,
          status_code=status.HTTP_201_CREATED)
def create_menus(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    return crud.create_menu(db=db, menu=menu)


@app.patch('/api/v1/menus/{menu_id}', response_model=schemas.Menu)
def update_menu(menu_id: str, menu: schemas.MenuBase,
                db: Session = Depends(get_db)):
    one_menu = crud.update_menu(db=db, id=menu_id, menu=menu)
    count_sub = crud.count_submenus(db=db, id=menu_id)
    count_dish = crud.count_dishes(db=db, id=menu_id)
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return schemas.Menu(id=menu_id, title=one_menu.title,
                        description=one_menu.description,
                        submenus_count=count_sub, dishes_count=count_dish)


@app.delete('/api/v1/menus/{menu_id}')
def delete_menu(menu_id: str, db: Session = Depends(get_db)):
    return crud.delete_menu(db=db, id=menu_id)


@app.get('/api/v1/menus/{menu_id}/submenus',
         response_model=list[schemas.SubMenu])
def get_submenus(menu_id: str, db: Session = Depends(get_db)):
    submenu = crud.get_submenus(db=db)
    response = []
    for value in submenu:
        response.append(
            schemas.Menu(id=value.id, title=value.title,
                         description=value.description,
                         dishes_count=crud.dishes_for_submenu(
                             db=db, id=value.id)))
    return response


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}',
         response_model=schemas.SubMenu)
def get_one_submenu(submenu_id: str, db: Session = Depends(get_db)):
    submenu = crud.get_one_submenu(db=db, id=submenu_id)
    dish_count = crud.dishes_for_submenu(db=db, id=submenu_id)
    return schemas.Menu(id=submenu.id, title=submenu.title,
                        description=submenu.description,
                        dishes_count=dish_count)


@app.post('/api/v1/menus/{menu_id}/submenus', response_model=schemas.SubMenu,
          status_code=status.HTTP_201_CREATED)
def create_submenu(submenu: schemas.SubMenuCreate, menu_id: str,
                   db: Session = Depends(get_db)):
    return crud.create_submenu(db=db, submenu=submenu, parent_id=menu_id)


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}',
           response_model=schemas.SubMenu)
def update_submenu(submenu: schemas.SubmenuBase, menu_id: str, submenu_id: str,
                   db: Session = Depends(get_db)):
    submenu = crud.update_submenu(db=db, submenu=submenu, id=submenu_id)
    dish_count = crud.dishes_for_submenu(db=db, id=submenu_id)
    return schemas.Menu(id=submenu.id, title=submenu.title,
                        description=submenu.description,
                        dishes_count=dish_count)


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def delete_submenu(submenu_id: str, db: Session = Depends(get_db)):
    return crud.delete_submenu(db=db, id=submenu_id)


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
         response_model=list[schemas.Dish])
def get_dishes(db: Session = Depends(get_db)):
    return crud.get_dishes(db=db)


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
         response_model=schemas.Dish)
def get_one_dish(dish_id: str, db: Session = Depends(get_db)):
    return crud.get_one_dish(db=db, id=dish_id)


@app.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
          response_model=schemas.Dish, status_code=status.HTTP_201_CREATED)
def create_dish(submenu_id: str, dish: schemas.DishCreate,
                db: Session = Depends(get_db)):
    return crud.create_dish(db=db, dish=dish, parent_id=submenu_id)


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
           response_model=schemas.Dish)
def update_dish(dish: schemas.DishBase, dish_id: str,
                db: Session = Depends(get_db)):
    return crud.update_dish(db=db, id=dish_id, dish=dish)


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def delete_dish(dish_id: str, db: Session = Depends(get_db)):
    return crud.delete_dish(db=db, id=dish_id)
