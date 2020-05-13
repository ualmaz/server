from django import template
from users.models import User

register = template.Library()

@register.simple_tag
def id_list():

    return User.objects.filter(pk__in=[2, 5])