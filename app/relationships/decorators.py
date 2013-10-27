from django.shortcuts import get_object_or_404
from app.users.models import SiteUser

def require_user(view):
    def inner(request, email, *args, **kwargs):
        user = get_object_or_404(SiteUser, email=email)
        return view(request, user, *args, **kwargs)
    return inner
