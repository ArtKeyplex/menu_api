import pytest
import uuid
import requests
from app.utils import ENDPOINT

@pytest.fixture()
def info_for_menu():
    return {
        'title': 'My great menu',
        'description': 'Hot Food'
    }


@pytest.fixture()
def info_for_submenu():
    result_str = f'test_title{uuid.uuid4().hex}'
    return {
        'title': f'{result_str}',
        'description': 'Meat'
    }


@pytest.fixture()
def info_for_dishes():
    result_str = f'test_title{uuid.uuid4().hex}'
    return {
        "title": f"{result_str}",
        "description": "My dish description 1",
        "price": "12.50"
    }


@pytest.fixture()
def get_menu_id(info_for_menu):
    create_response = requests.post(ENDPOINT + '/menus', json=info_for_menu)
    return create_response.json()['id']


@pytest.fixture()
def get_submenu_id(get_menu_id, info_for_submenu):
    menu_id = get_menu_id
    create_response = requests.post(ENDPOINT + f'/menus/{menu_id}/submenus',
                                    json=info_for_submenu)
    return create_response.json()['id']


@pytest.fixture()
def get_dish_id(get_menu_id, get_submenu_id, info_for_dishes):
    create_response = requests.post(
        ENDPOINT + f'/menus/{get_menu_id}/submenus/{get_submenu_id}/dishes',
        json=info_for_dishes)
    return create_response.json()['id']


@pytest.fixture(scope='session')
def create_menu(info_for_menu):
    yield

