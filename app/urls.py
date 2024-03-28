from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView, TemplateView

from app.views import DemoPageView, auth_page_view, page_view, error_view

urlpatterns = [
    # заменить на app/page.html и проверить настройки TEMPLATES - DIRS
    path("page/", TemplateView.as_view(template_name="page.html"), name="page"),
    # страница с template tags и context processors
    path("demo-page/", DemoPageView.as_view(), name="demo-page"),
    # примеры страниц, закрытых авторизацией
    path("auth1/", login_required(page_view), name="auth1"),
    path("auth2/", auth_page_view, name="auth2"),
    # редирект
    path(
        "page-redirect/",
        RedirectView.as_view(url=reverse_lazy("page")),
        name="page-redirect",
    ),
    # страница с ошибкой 500
    path("error/", error_view, name="error-500"),
]
