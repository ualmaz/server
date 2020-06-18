import calendar
from django import template
from users.models import User

register = template.Library()

@register.simple_tag
def id_list():
    return User.objects.filter(pk__in=[2, 5])

@register.filter
def month_name(month_number):
    return calendar.month_name[month_number]
