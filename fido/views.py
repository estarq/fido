from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from common.decorators import shelter_required
from .forms import ContactForm, ShelterAddressForm, ShelterForm
from .models import Shelter, ShelterAddress


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'fido/contact.html', {'form': ContactForm(), 'sent': True})
        return render(request, 'fido/contact.html', {'form': form, 'sent': False})

    return render(request, 'fido/contact.html', {'form': ContactForm()})


@login_required
def new_shelter(request):
    try:
        shelter = Shelter.objects.get(owner=request.user)
    except Shelter.DoesNotExist:
        pass
    else:
        return redirect('fido:shelter', pk=shelter.pk)

    if request.method == 'POST':
        shelter_form = ShelterForm(request.POST)
        address_form = ShelterAddressForm(request.POST)
        if shelter_form.is_valid() and address_form.is_valid():
            shelter = shelter_form.save(commit=False)
            shelter.owner = request.user
            shelter.save()
            address = address_form.save(commit=False)
            address.shelter = shelter
            address.save()
            return redirect('fido:shelter', pk=shelter.pk)
        context = {'forms': [shelter_form, address_form]}
        return render(request, 'fido/new-shelter.html', context)

    context = {'forms': [ShelterForm(), ShelterAddressForm()]}
    return render(request, 'fido/new-shelter.html', context)


def pet(request, pk, model):
    context = {'pet': get_object_or_404(model, pk=pk)}
    return render(request, 'fido/pet.html', context)


def shelter_page(request, pk):
    context = {
        'shelter': get_object_or_404(Shelter, pk=pk),
        'address': ShelterAddress.objects.get(shelter=pk),
    }
    return render(request, 'fido/shelter.html', context)


@login_required
@shelter_required
def edit_shelter(request):
    if request.method == 'POST':
        shelter_form = ShelterForm(request.POST)
        address_form = ShelterAddressForm(request.POST)
        if shelter_form.is_valid() and address_form.is_valid():
            shelter = Shelter.objects.filter(owner=request.user)
            address = ShelterAddress.objects.filter(shelter=shelter.first())
            shelter.update(**shelter_form.cleaned_data)
            address.update(**address_form.cleaned_data)
            return redirect('fido:shelter', pk=shelter.first().pk)
        context = {'forms': [shelter_form, address_form]}
        return render(request, 'fido/edit-shelter.html', context)

    shelter = Shelter.objects.get(owner=request.user)
    shelter_form = ShelterForm(instance=shelter)
    address_form = ShelterAddressForm(instance=shelter.shelteraddress)
    context = {'forms': [shelter_form, address_form]}
    return render(request, 'fido/edit-shelter.html', context)
