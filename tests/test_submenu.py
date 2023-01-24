import pytest
import uuid
from app.utils import ENDPOINT
from .fake_db import client


@pytest.fixture(autouse=True)
def clean(get_menu_id):
    yield
    delete_menu(get_menu_id)


class TestSubMenu:
    def test_get_list_submenus(self, info_for_submenu, get_menu_id):
        n = 3
        menu_id = get_menu_id
        for _ in range(n):
            info_for_submenu['title'] = f'test_title{uuid.uuid4().hex}'
            create_response = create_submenu(menu_id, info_for_submenu)
            assert create_response.status_code == 201
        list_response = list_submenu(menu_id)
        assert list_response.status_code == 200
        data = list_response.json()
        assert len(data) == n

    def test_get_submenu(self, info_for_submenu, get_submenu_id, get_menu_id):
        menu_id = get_menu_id
        submenu_id = get_submenu_id
        get_submenu_response = get_submenu(menu_id, submenu_id)
        assert get_submenu_response.status_code == 200
        get_data = get_submenu_response.json()
        assert get_data['title'] == info_for_submenu['title']
        assert get_data['description'] == info_for_submenu['description']

    def test_create_submenu(self, info_for_submenu,
                            get_menu_id):
        create_response = create_submenu(get_menu_id, info_for_submenu)
        assert create_response.status_code == 201
        create_data = create_response.json()
        assert create_data['title'] == info_for_submenu['title']
        assert create_data['description'] == info_for_submenu['description']

    def test_update_submenu(self, info_for_submenu, get_menu_id,
                            get_submenu_id):
        menu_id = get_menu_id
        submenu_id = get_submenu_id
        new_submenu = {
            'title': 'Pirozhki',
            'description': 'Wow!'
        }
        update_response = update_submenu(menu_id, submenu_id, new_submenu)
        assert update_response.status_code == 200
        get_response = get_submenu(menu_id, submenu_id)
        assert get_response.status_code == 200
        get_data = get_response.json()
        assert get_data['title'] == new_submenu['title']
        assert get_data['description'] == new_submenu['description']

    def test_delete_submenu(self, get_menu_id, get_submenu_id):
        delete_response = delete_submenu(get_menu_id, get_submenu_id)
        assert delete_response.status_code == 200
        submenu = get_submenu(get_menu_id, get_submenu_id)
        assert submenu.status_code == 404


def create_menu(info):
    return client.post(ENDPOINT + '/menus', json=info)


def delete_menu(menu_id):
    return client.delete(ENDPOINT + f'/menus/{menu_id}')


def create_submenu(menu_id, info_submenu):
    return client.post(ENDPOINT + f'/menus/{menu_id}/submenus',
                         json=info_submenu)


def update_submenu(menu_id, submenu_id, info):
    return client.patch(ENDPOINT + f'/menus/{menu_id}/submenus/{submenu_id}',
                          json=info)


def list_submenu(menu_id):
    return client.get(ENDPOINT + f'/menus/{menu_id}/submenus')


def get_submenu(menu_id, submenu_id):
    return client.get(ENDPOINT + f'/menus/{menu_id}/submenus/{submenu_id}')


def delete_submenu(menu_id, submenu_id):
    return client.delete(
        ENDPOINT + f'/menus/{menu_id}/submenus/{submenu_id}'
    )