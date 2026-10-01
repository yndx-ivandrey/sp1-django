from django.urls import include, path

from .views import SignUpView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    # стандартные url для работы с пользователями
    path("", include("django.contrib.auth.urls")),
]
