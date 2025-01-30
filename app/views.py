from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


def not_found_view(request: HttpRequest, exception=None) -> HttpResponse:
    return render(
        request,
        "404.html",
        status=404,
        context={"request_path": request.path, "extra": "custom 404 manager"},
    )


def server_error_value_view(request: HttpRequest) -> HttpResponse:
    # raise Exception("Ha-Ha-Ha!")
    return render(None, "500.html", status=500)


class DemoPageView(TemplateView):
    template_name = "app/demo-page.html"


@login_required
def auth_page_view(request: HttpRequest) -> HttpResponse:
    return render(request, "auth_page.html")


def page_view(request: HttpRequest) -> HttpResponse:
    return render(request, "auth_page.html")


def error_view(request: HttpRequest) -> HttpResponse:
    raise Exception("Unexpected server failure!")
