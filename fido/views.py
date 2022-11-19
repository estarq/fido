from itertools import chain

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404

from common.decorators import shelter_required
from .forms import (ContactForm, CatForm, DogForm, EditCatForm, EditDogForm, SearchCatsForm,
                    SearchDogsForm, ShelterAddressForm, ShelterForm)
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


def pet_page(request, pk, model):
    context = {'pet': get_object_or_404(model, pk=pk)}
    return render(request, 'fido/pet.html', context)


def shelter_page(request, pk):
    shelter = get_object_or_404(Shelter.objects.select_related('shelteraddress'), pk=pk)
    context = {
        'shelter': shelter,
        'address': shelter.shelteraddress,
        'page_obj': page_obj_all_pets(request, shelter),
    }
    return render(request, 'fido/shelter.html', context)


@login_required
@shelter_required
def manage_pets(request):
    page_obj = page_obj_all_pets(request, request.user.shelter)
    return render(request, 'fido/manage-pets.html', {'page_obj': page_obj})


def page_obj_all_pets(request, shelter):
    cats = Cat.objects.filter(shelter=shelter)
    dogs = Dog.objects.filter(shelter=shelter)
    # cats.union(dogs) makes Dogs appear to be Cats and breaks a custom filter
    pets = sorted(chain(cats, dogs), key=lambda pet: -pet.pk)
    return Paginator(pets, 12).get_page(request.GET.get('page'))


def search_cats(request):
    model = Cat
    context = {
        'form': SearchCatsForm(),
        'pet_url': 'fido:cat',
        'name_plural': 'cats',
        'approx_pet_count': 37500,
    }
    return search_pets(request, model, context)


def search_dogs(request):
    model = Dog
    context = {
        'form': SearchDogsForm(),
        'pet_url': 'fido:dog',
        'name_plural': 'dogs',
        'approx_pet_count': 21700,
    }
    return search_pets(request, model, context)


def search_pets(request, model, context):
    pets = model.objects.all().order_by('-pk')
    paginator = Paginator(pets, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context.update(page_obj=page_obj)
    return render(request, 'fido/search-pets.html', context)


def search_cats_params(request, **kwargs):
    model = Cat
    form_class = SearchCatsForm
    context = {
        'pet_url': 'fido:cat',
        'name_plural': 'cats',
        'approx_pet_count': 37500,
    }
    return search_pets_params(request, model, form_class, context, **kwargs)


def search_dogs_params(request, **kwargs):
    model = Dog
    form_class = SearchDogsForm
    context = {
        'pet_url': 'fido:dog',
        'name_plural': 'dogs',
        'approx_pet_count': 21700,
    }
    return search_pets_params(request, model, form_class, context, **kwargs)


def search_pets_params(request, model, form_class, context, **kwargs):
    kwargs = {k: v.replace('-', ' ') for k, v in kwargs.items()}
    form = form_class(data=kwargs)
    if not form.is_valid():
        raise SuspiciousOperation
    pets = model.objects.filter(**kwargs).select_related('shelter__shelteraddress').order_by('-pk')
    paginator = Paginator(pets, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context.update(form=form, page_obj=page_obj)
    return render(request, 'fido/search-pets.html', context)


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
def remove_shelter(request):
    shelter = Shelter.objects.get(owner=request.user)
    if request.method == 'POST':
        shelter.delete()
        return redirect('fido:homepage')

    cat_count = Cat.objects.filter(shelter=shelter).count()
    dog_count = Dog.objects.filter(shelter=shelter).count()
    context = {
        'shelter': shelter,
        'count': cat_count + dog_count,
    }
    return render(request, 'fido/remove-shelter.html', context)


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


@login_required
@shelter_required
def remove_pet(request, pk, model):
    pet = get_object_or_404(model, pk=pk)
    if pet.shelter != request.user.shelter:
        raise PermissionDenied

    if request.method == 'POST':
        pet.delete()
        return redirect('fido:manage-pets')

    return render(request, 'fido/remove-pet.html', {'pet': pet})
