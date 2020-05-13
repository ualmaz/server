from .models import User

def users_id_list(request):
    user = User
    return {'users_id_list': User.objects.filter(pk__in=[1, 2])}