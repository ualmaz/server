from django import template
from video.models import User

register = template.Library()

@register.simple_tag
def id_list():

    return User.objects.filter(pk__in=[2, 5])