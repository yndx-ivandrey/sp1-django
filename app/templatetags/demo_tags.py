from typing import Any

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


__MONTH_LIST = [
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
]


@register.filter(name="month_str")
def month2str(value: Any) -> str:
    try:
        return __MONTH_LIST[int(value)]
    except TypeError:
        return "Month should be a number!"
    except IndexError:
        return f"There is no month with {value} index!"


@register.filter()
@stringfilter
def replace_with_hash(value: str, substring: str) -> str:
    return value.replace(substring, "#")


@register.simple_tag(takes_context=True)
def user_agent(context) -> str:
    return context.request.META["HTTP_USER_AGENT"]
