
#  REST API Меню ресторана

Проект на FastAPI с использованием PostgreSQL в качестве БД.
В проекте реализовано REST API по работе с меню ресторана, все CRUD операции.


Стек технологий
----------
* Python 3.11
* FastAPI 
* Pydentic
* Starlette
* PostgreSQL
* SQLAlchemy
* Uvicorn

Установка проекта из репозитория
----------

1. Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone git@github.com:ArtKeyplex/menu_api.git

```
2. Cоздать и активировать виртуальное окружение:
```bash
python3 -m venv venv

source venv/bin/activate
```
3. Установить зависимости из файла ```requirements.txt```:
```bash
python3 -m pip install --upgrade pip

pip install -r requirements.txt

```
4. Перейти в директорию с проектом
```
cd app
```
5. Создать .env со следующими параметрами:
```
database_hostname=db
database_password=postgres
database_name=fastapi
database_username=postgres
```
6. Запустить проект:
```bash
docker-compose up -d
```
7. Запустить тесты:
```bash
docker-compose -f docker-compose.tests.yml up -d
```
