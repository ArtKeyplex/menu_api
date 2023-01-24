import requests
import pytest
import uuid
from app.utils import ENDPOINT


@pytest.fixture(autouse=True)
def clean(get_menu_id):
    yield
    delete_menu(get_menu_id)


class TestDishes:
    def test_get_list_dishes(self, info_for_dishes, get_menu_id, get_submenu_id):
        n = 3

        for _ in range(n):
            info_for_dishes['title'] = f'test_title{uuid.uuid4().hex}'
            create_response = create_dish(get_menu_id, get_submenu_id, info_for_dishes)
            assert create_response.status_code == 201
        list_response = list_dishes(get_menu_id, get_submenu_id)
        assert list_response.status_code == 200
        data = list_response.json()
        assert len(data) == n

    def test_get_dish(self, info_for_dishes, get_menu_id, get_dish_id, get_submenu_id):
        get_response = get_dish(get_menu_id, get_submenu_id, get_dish_id)
        assert get_response.status_code == 200
        get_data = get_response.json()
        assert get_data['title'] == info_for_dishes['title']
        assert get_data['description'] == info_for_dishes['description']

    def test_create_dish(self, info_for_dishes, get_menu_id, get_submenu_id):
        create_response = create_dish(get_menu_id, get_submenu_id, info_for_dishes)
        assert create_response.status_code == 201
        create_data = create_response.json()
        assert create_data['title'] == info_for_dishes['title']
        assert create_data['title'] == info_for_dishes['title']

    def test_update_dish(self, info_for_dishes, get_menu_id, get_submenu_id,
                         get_dish_id):
        new_dish = {
            "title": "My updated dish 1",
            "description": "My updated dish description 1",
            "price": "14.50"
        }

        update_response = update_dish(
            get_menu_id, get_submenu_id, get_dish_id, new_dish
        )
        assert update_response.status_code == 200
        update_data = update_response.json()
        assert update_data['title'] == new_dish['title']
        assert update_data['title'] == new_dish['title']

    def test_delete_dish(self, get_menu_id, get_submenu_id, get_dish_id):
        delete_response = delete_dish(get_menu_id, get_submenu_id, get_dish_id)
        assert delete_response.status_code == 200
        dish = get_dish(get_menu_id, get_submenu_id, get_dish_id)
        assert dish.status_code == 404


def create_menu(info):
    return requests.post(ENDPOINT + '/menus', json=info)


def delete_menu(menu_id):
    return requests.delete(ENDPOINT + f'/menus/{menu_id}')


def create_submenu(menu_id, info_submenu):
    return requests.post(ENDPOINT + f'/menus/{menu_id}/submenus',
                         json=info_submenu)


def create_dish(menu_id, submenu_id, info_dish):
    return requests.post(
        ENDPOINT + f'/menus/{menu_id}/submenus/{submenu_id}/dishes',
        json=info_dish
    )


def update_dish(menu_id, submenu_id, dish_id, info):
    return requests.patch(
        ENDPOINT + f'/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
        json=info
    )


def list_dishes(menu_id, submenu_id):
    return requests.get(
        ENDPOINT + f'/menus/{menu_id}/submenus/{submenu_id}/dishes'
    )


def get_dish(menu_id, submenu_id, dish_id):
    return requests.get(
        ENDPOINT + f'/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
    )


def delete_dish(menu_id, submenu_id, dish_id):
    return requests.delete(
        ENDPOINT + f'/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
    )
