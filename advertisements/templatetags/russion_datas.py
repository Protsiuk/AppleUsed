from django import template

from datetime import datetime, timedelta, date

register = template.Library()


@register.filter(is_safe=True)
def russian_date(value):
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    print(value)
    if value.strftime("%d.%m.%Y") == now.strftime("%d.%m.%Y"):
        return "сегодня"
    elif value.strftime("%d.%m.%Y") == yesterday.strftime("%d.%m.%Y"):
        return "вчера"
    else:
        return value.strftime("%d.%m.%Y")

