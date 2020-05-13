from .models import User

def users_id_list(request):
    
    user = User.objects.filter(pk__in=[2, 5])

    context = {
        'users_id_list': user
    }

    return context