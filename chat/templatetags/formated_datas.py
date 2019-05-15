from django import template

from datetime import datetime, timedelta, date

register = template.Library()


@register.assignment_tag()
def last_message(value):
    last_message = value.objects.order_by("-id")[0:1]
    return {
        'last_message': last_message,
    }


@register.filter(is_safe=True)
def formated_datas(value):
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    # print('ЗНАЧЕНИЕ VALUE', value)
    if value.strftime('%d.%m.%Y') == now.strftime("%d.%m.%Y"):
        return "сегодня"
    elif value.strftime("%d.%m.%Y") == yesterday.strftime("%d.%m.%Y"):
        return "вчера"
    else:
        return value.strftime("%d.%m.%Y")


# @register.filter(is_safe=True)
# def formated_datas(value):
#     # print('TYPE OF DATE IS -', type(value))
#     now = datetime.now()
#     yesterday = now - timedelta(days=1)
#     if type(value) is str:
#         # print('ISstring')
#         value = value.strptime()
#     #     print(type(value))
#     # print('TYPE OF DATE IS -', type(value))
#     # print('ЗНАЧЕНИЕ VALUE', value)
#     if value.strftime('%d.%m.%Y') == now.strftime("%d.%m.%Y"):
#         return "сегодня"
#     elif value.strftime("%d.%m.%Y") == yesterday.strftime("%d.%m.%Y"):
#         return "вчера"
#     else:
#         return value.strftime("%d.%m.%Y")
