from django.shortcuts import render

from fido.models import Dog
from .forms import ContactForm


# Create your views here.
def index(request):
    dogs = Dog.objects.all()
    return render(request, 'fido/index.html', {'dogs': dogs})


def for_shelters(request):
    return render(request, 'fido/for-shelters.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            form = ContactForm()
            return render(request, 'fido/contact.html', {'form': form, 'sent': True})
        return render(request, 'fido/contact.html', {'form': form, 'sent': False})

    form = ContactForm()
    return render(request, 'fido/contact.html', {'form': form})
