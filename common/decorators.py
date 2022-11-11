from functools import wraps

from django.shortcuts import redirect

from fido.models import Shelter


def shelter_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if Shelter.objects.filter(owner=request.user).exists():
            return view_func(request, *args, **kwargs)
        return redirect('fido:new-shelter')

    return wrapper
