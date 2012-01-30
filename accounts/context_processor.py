from accounts.models import UserProfile

def user(request):
    if request.user.id != None and not request.user.is_staff:
        id_ = UserProfile.objects.get(user = request.user).social_id
        return {'username' : request.user.username, "id_" : id_}
    return {}
