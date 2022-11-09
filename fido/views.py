from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ContactForm, NewShelterAddressForm, NewShelterForm
from .models import Shelter


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


@login_required
def new_shelter(request):
    if Shelter.objects.filter(owner=request.user).exists():
        return redirect('fido:homepage')

    if request.method == 'POST':
        shelter_form = NewShelterForm(request.POST)
        address_form = NewShelterAddressForm(request.POST)
        if shelter_form.is_valid() and address_form.is_valid():
            shelter = shelter_form.save(commit=False)
            shelter.owner = request.user
            shelter.save()
            address = address_form.save(commit=False)
            address.shelter = shelter
            address.save()
            return redirect('fido:homepage')
        context = {'forms': [shelter_form, address_form]}
        return render(request, 'fido/new-shelter.html', context)

    shelter_form = NewShelterForm()
    address_form = NewShelterAddressForm()
    context = {'forms': [shelter_form, address_form]}
    return render(request, 'fido/new-shelter.html', context)
