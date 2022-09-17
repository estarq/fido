from django.shortcuts import render
from fido.models import Dog


# Create your views here.
def index(request):
    dogs = Dog.objects.all()
    return render(request, 'fido/index.html', {'dogs': dogs})
