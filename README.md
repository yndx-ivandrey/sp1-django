# Демо для вебинара по Django

Ожидаем python 3.12.x

```
python -m venv venv
source ./venv/bin/activate
pip install poetry
poetry install --no-root
python manage.py runserver
```
Доступ в /admin/ -   логин admin / пароль admin

### Игры с поиском шаблона для страницы /app/page/
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

### Игры со страницами ошибок:
1. установить `DEBUG = False` в settings.py
2. переименовать templates/400_.html в templates/400.html и templates/500_.html в templates/500.html
3. раскомментировать в sp1_demo/urls.py handler404/handler500
4. раскомментировать в app/views.py Exception в server_error_value_view

### flatpages:
/pages/page1/ - обычная страница
/pages/super/ - закрыта авторизацией

