from datetime import datetime
from zoneinfo import ZoneInfo

from django.http.request import HttpRequest


def source_ip_processor(request: HttpRequest) -> dict[str, str]:
    return {
        "source_ip": request.META["REMOTE_ADDR"],
    }


def current_time_processor(request: HttpRequest) -> dict[str, str]:
    return {
        "time": datetime.now(tz=ZoneInfo("Europe/Moscow")).isoformat(),
    }
