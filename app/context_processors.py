from datetime import datetime


def source_ip_processor(request):
    return {
        "source_ip": request.META["REMOTE_ADDR"],
    }


def current_time_processor(request):
    return {
        "time": datetime.now().isoformat(),
    }
