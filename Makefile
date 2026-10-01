# Нужно активное виртуальное окружение для python

UVSYNC ?= uv sync --frozen
PYTHON ?= uv run python
MANAGE = $(PYTHON) manage.py

ADMIN_USERNAME = admin
ADMIN_EMAIL = admin@test.test
ADMIN_PASSWORD = admin

.PHONY: help clean init run

help:
	@echo "make init   - пересоздать базу, суперпользователя и тестовые данные"
	@echo "make clean  - удалить db.sqlite3 и все медиафайлы"
	@echo "make run    - запустить сервер разработки"

# Удаляет базу данных и все загруженные медиафайлы
clean:
	rm -f db.sqlite3 db.sqlite3-*
	rm -rf media

# Полная переинициализация: clean -> migrate -> суперпользователь -> тестовые данные
init: export DJANGO_SUPERUSER_PASSWORD := $(ADMIN_PASSWORD)
init: clean
	$(PYTHON ?= uv run pythonUVSYNC)
	$(MANAGE) migrate
	$(MANAGE) createsuperuser --noinput --username $(ADMIN_USERNAME) --email $(ADMIN_EMAIL)
	$(MANAGE) generate_blog_data

# Локальный сервер разработки
run:
	$(MANAGE) runserver
