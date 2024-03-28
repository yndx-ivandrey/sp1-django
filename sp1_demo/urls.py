from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from sp1_demo import settings

# Кастомизированные страницы ошибок
# handler404 = "app.views.not_found_view"
# handler500 = "app.views.server_error_value_view"

urlpatterns = [
    # наше тестовое приложение
    path("app/", include("app.urls")),
    # домашняя страница
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path("admin/", admin.site.urls),
    # переопределение для регистрации
    path("accounts/", include("accounts.urls")),
    # стандартные url для работы с пользователями
    path("accounts/", include("django.contrib.auth.urls")),
    # flat pages
    path("pages/", include("django.contrib.flatpages.urls")),
]

if settings.DEBUG:
    urlpatterns = [
        path("__debug__/", include("debug_toolbar.urls")),
    ] + urlpatterns
