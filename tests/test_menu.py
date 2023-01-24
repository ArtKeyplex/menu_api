import pytest
from app.utils import ENDPOINT
from .fake_db import client


@pytest.fixture()
def clean(get_menu_id):
    yield
    delete_menu(get_menu_id)


class TestMenu:
    def test_get_list_menu(self, info_for_menu):
        n = 3
        for _ in range(n):
            create_response = create_menu(info=info_for_menu)
            assert create_response.status_code == 201
        list_response = list_menu()
        assert list_response.status_code == 200
        data = list_response.json()
        for i in data:
            delete_menu(i['id'])
        assert len(data) == n

    def test_get_menu(self, info_for_menu, get_menu_id):
        menu_id = get_menu_id
        get_response = get_menu(menu_id=menu_id)
        assert get_response.status_code == 200
        get_data = get_response.json()
        assert get_data['title'] == info_for_menu['title']
        assert get_data['description'] == info_for_menu['description']
        delete_menu(menu_id)

    def test_create_menu(self, info_for_menu):
        create_response = create_menu(info_for_menu)
        assert create_response.status_code == 201
        data = create_response.json()
        menu_id = data['id']
        get_response = get_menu(menu_id=menu_id)
        assert get_response.status_code == 200
        get_data = get_response.json()
        assert get_data['title'] == info_for_menu['title']
        assert get_data['description'] == info_for_menu['description']
        delete_menu(get_data['id'])

    def test_menu_update(self, info_for_menu, get_menu_id):
        menu_id = get_menu_id
        new_menu = {
            'title': 'Updated title',
            'description': 'updated description'
        }
        update_response = update_menu(info=new_menu, id=menu_id)
        assert update_response.status_code == 200
        get_response = get_menu(menu_id=menu_id)
        assert get_response.status_code == 200
        get_data = get_response.json()
        assert get_data['title'] == new_menu['title']
        assert get_data['description'] == new_menu['description']
        delete_menu(get_data['id'])

    def test_menu_delete(self, get_menu_id):
        delete_response = delete_menu(get_menu_id)
        assert delete_response.status_code == 200
        menu = get_menu(get_menu_id)
        assert menu.status_code == 404


def create_menu(info):
    return client.post(ENDPOINT + '/menus',
                         json=info)


def update_menu(info, id):
    return client.patch(ENDPOINT + f'/menus/{id}', json=info)


def get_menu(menu_id):
    return client.get(ENDPOINT + f'/menus/{menu_id}')


def list_menu():
    return client.get(ENDPOINT + '/menus')


def delete_menu(menu_id):
    return client.delete(ENDPOINT + f'/menus/{menu_id}')
