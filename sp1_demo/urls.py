from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
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
    # админка
    path("admin/", admin.site.urls),
    # кастомная модель пользователей
    path("accounts/", include("accounts.urls")),
    # flat pages
    path("pages/", include("django.contrib.flatpages.urls")),
    # приложение с блогом
    path("blog/", include("blog.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = [
        path("__debug__/", include("debug_toolbar.urls")),
    ] + urlpatterns
