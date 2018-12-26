from django import template

from datetime import datetime, timedelta, date

register = template.Library()


@register.filter(is_safe=True)
def formated_datas(value):
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    print('ЗНАЧЕНИЕ VALUE', value)
    if value.strftime('%d.%m.%Y') == now.strftime("%d.%m.%Y"):
        return "сегодня"
    elif value.strftime("%d.%m.%Y") == yesterday.strftime("%d.%m.%Y"):
        return "вчера"
    else:
        return value.strftime("%d.%m.%Y")

