import uuid
import requests
from app.utils import ENDPOINT
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from sqlalchemy_utils import database_exists, create_database
from app.config import settings
from app.database import get_db
from app.database import Base


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


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


