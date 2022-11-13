from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render, get_object_or_404

from common.decorators import shelter_required
from .forms import ContactForm, CatForm, DogForm, EditCatForm, EditDogForm, ShelterAddressForm, ShelterForm
from .models import Cat, Dog, Shelter, ShelterAddress


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


@login_required
@shelter_required
def new_cat(request):
    context = {
        'title': 'New Cat',
        'headline': 'New Cat',
    }

    if request.method == 'POST':
        form = CatForm(request.POST, request.FILES)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.shelter = request.user.shelter
            cat.save()
            return redirect('fido:cat', pk=cat.pk)
        context.update(form=form)
        return render(request, 'fido/form.html', context)

    context.update(form=CatForm())
    return render(request, 'fido/form.html', context)


@login_required
@shelter_required
def new_dog(request):
    context = {
        'title': 'New Dog',
        'headline': 'New Dog',
    }

    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            dog = form.save(commit=False)
            dog.shelter = request.user.shelter
            dog.save()
            return redirect('fido:dog', pk=dog.pk)
        context.update(form=form)
        return render(request, 'fido/form.html', context)

    context.update(form=DogForm())
    return render(request, 'fido/form.html', context)


@login_required
@shelter_required
def edit_cat(request, pk):
    cat = get_object_or_404(Cat, pk=pk)
    if cat.shelter != request.user.shelter:
        raise PermissionDenied

    context = {
        'title': 'Edit Cat',
        'headline': 'Cat Details',
    }

    if request.method == 'POST':
        form = EditCatForm(request.POST, request.FILES)
        if form.is_valid():
            cat = Cat.objects.filter(pk=pk)
            cat.update(**form.cleaned_data)
            return redirect('fido:cat', pk=pk)
        context.update(form=form)
        return render(request, 'fido/form.html', context)

    context.update(form=EditCatForm(instance=cat))
    return render(request, 'fido/form.html', context)


@login_required
@shelter_required
def edit_dog(request, pk):
    dog = get_object_or_404(Dog, pk=pk)
    if dog.shelter != request.user.shelter:
        raise PermissionDenied

    context = {
        'title': 'Edit Dog',
        'headline': 'Dog Details',
    }

    if request.method == 'POST':
        form = EditDogForm(request.POST, request.FILES)
        if form.is_valid():
            dog = Dog.objects.filter(pk=pk)
            dog.update(**form.cleaned_data)
            return redirect('fido:dog', pk=pk)
        context.update(form=form)
        return render(request, 'fido/form.html', context)

    context.update(form=EditDogForm(instance=dog))
    return render(request, 'fido/form.html', context)
