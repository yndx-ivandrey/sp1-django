# Демо для вебинара по Django

Ожидаем наличие uv и python 3.14.x
Запуск (linux / macOS):
```bash
make init
make run
```
В windows:
```commandline
uv sync --frozen
uv run python manage.py migrate
uv run python manage.py createsuperuser --username admin --email 'admin@test.test'
uv run python manage.py generate_blog_data
uv run python manage.py runserver
```
Доступ в /admin/ -   логин admin / пароль admin (или заданный при создании супер-пользователя)

### Приоритеты шаблонов при конфликте между приложениями - страница /app/page/
1. в setting.py указать `"DIRS": [],`
2. включить приложение app1 в settings.py
3. заменить url в app/urls.py на `app/page.html`
4. включить обратно DIRS в settings.py

/app/demo-page/  - context processor + template tags

/app/auth1/ - ссылка за авторизацией
/app/auth2/ - ссылка за авторизацией

/accounts/signup/ - регистрация

/app/page-redirect/ - редирект на страницу /app/page/

/accounts/password_reset/  - "встроенная" форма для смены пароля

/accounts/password_reset/  - "встроенная" форма для восстановления пароля

### Страницы ошибок:
1. установить `DEBUG = False` в settings.py
2. переименовать templates/400_.html в templates/400.html и templates/500_.html в templates/500.html
3. раскомментировать в sp1_demo/urls.py handler404/handler500
4. раскомментировать в app/views.py Exception в server_error_value_view

### /blog - мини-приложение для ведения блога
