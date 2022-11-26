from itertools import chain

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404

from common.constants import APPROX_CAT_COUNT, APPROX_DOG_COUNT, PETS_PER_PAGE
from common.decorators import redirect_if_shelter, shelter_required
from .forms import (ContactForm, CatForm, DogForm, EditCatForm, EditDogForm, SearchCatsForm,
                    SearchDogsForm, ShelterAddressForm, ShelterForm)
from .models import Cat, Dog, Shelter, ShelterAddress


def contact(request):
    if request.method == 'POST':
        return contact_post(request)
    return contact_get(request)


def contact_get(request):
    context = {'form': ContactForm()}
    return render(request, 'fido/contact.html', context)


def contact_post(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        form.save()
        context = {'form': ContactForm(), 'sent': True}
    else:
        context = {'form': form, 'sent': False}
    return render(request, 'fido/contact.html', context)


def cat_page(request, pk):
    return pet_page(request, pk, Cat)


def dog_page(request, pk):
    return pet_page(request, pk, Dog)


def pet_page(request, pk, model):
    context = {'pet': get_object_or_404(model, pk=pk)}
    return render(request, 'fido/pet.html', context)


def search_cats(request):
    context = {
        'form': SearchCatsForm(),
        'pet_url': 'fido:cat',
        'name_plural': 'cats',
        'approx_pet_count': APPROX_CAT_COUNT,
    }
    return search_pets(request, Cat, context)


def search_dogs(request):
    context = {
        'form': SearchDogsForm(),
        'pet_url': 'fido:dog',
        'name_plural': 'dogs',
        'approx_pet_count': APPROX_DOG_COUNT,
    }
    return search_pets(request, Dog, context)


def search_pets(request, model, context):
    pets = model.objects.all().order_by('-pk')
    page_obj = Paginator(pets, PETS_PER_PAGE).get_page(request.GET.get('page'))
    context.update(page_obj=page_obj)
    return render(request, 'fido/search-pets.html', context)


def search_cats_params(request, **params):
    context = {
        'pet_url': 'fido:cat',
        'name_plural': 'cats',
        'approx_pet_count': APPROX_CAT_COUNT,
    }
    return search_pets_params(request, Cat, SearchCatsForm, context, **params)


def search_dogs_params(request, **params):
    context = {
        'pet_url': 'fido:dog',
        'name_plural': 'dogs',
        'approx_pet_count': APPROX_DOG_COUNT,
    }
    return search_pets_params(request, Dog, SearchDogsForm, context, **params)


def search_pets_params(request, model, form_class, context, **params):
    params = {k: v.replace('-', ' ') for k, v in params.items()}
    form = form_class(data=params)
    if not form.is_valid():
        raise SuspiciousOperation
    pets = model.objects.filter(**params).select_related('shelter__shelteraddress').order_by('-pk')
    page_obj = Paginator(pets, PETS_PER_PAGE).get_page(request.GET.get('page'))
    context.update(form=form, page_obj=page_obj)
    return render(request, 'fido/search-pets.html', context)


def shelter_page(request, pk):
    shelter = get_object_or_404(Shelter.objects.select_related('shelteraddress'), pk=pk)
    context = {
        'shelter': shelter,
        'address': shelter.shelteraddress,
        'page_obj': page_obj_all_pets(request, shelter),
    }
    return render(request, 'fido/shelter.html', context)


def page_obj_all_pets(request, shelter):
    cats = Cat.objects.filter(shelter=shelter)
    dogs = Dog.objects.filter(shelter=shelter)
    # cats.union(dogs) makes Dogs appear to be Cats and breaks a custom filter
    pets = sorted(chain(cats, dogs), key=lambda pet: -pet.pk)
    return Paginator(pets, PETS_PER_PAGE).get_page(request.GET.get('page'))


@login_required
@redirect_if_shelter
def new_shelter(request):
    context = {'title': 'New shelter', 'headline': 'Shelter Details'}
    if request.method == 'POST':
        return new_shelter_post(request, context)
    return new_shelter_get(request, context)


def new_shelter_get(request, context):
    context.update(forms=[ShelterForm(), ShelterAddressForm()])
    return render(request, 'fido/form.html', context)


def new_shelter_post(request, context):
    shelter_form = ShelterForm(request.POST)
    address_form = ShelterAddressForm(request.POST)
    if shelter_form.is_valid() and address_form.is_valid():
        shelter = shelter_form.save(commit=False)
        address = address_form.save(commit=False)
        shelter.owner = request.user
        address.shelter = shelter
        shelter.save()
        address.save()
        return redirect('fido:shelter', pk=shelter.pk)
    context.update(forms=[shelter_form, address_form])
    return render(request, 'fido/form.html', context)


@login_required
@shelter_required
def edit_shelter(request):
    context = {'title': 'Manage shelter', 'headline': 'Shelter Details'}
    if request.method == 'POST':
        return edit_shelter_post(request, context)
    return edit_shelter_get(request, context)


def edit_shelter_get(request, context):
    shelter = Shelter.objects.filter(owner=request.user).select_related('shelteraddress')
    shelter_form = ShelterForm(instance=shelter.first())
    address_form = ShelterAddressForm(instance=shelter.first().shelteraddress)
    context.update(forms=[shelter_form, address_form])
    return render(request, 'fido/form.html', context)


def edit_shelter_post(request, context):
    shelter_form = ShelterForm(request.POST)
    address_form = ShelterAddressForm(request.POST)
    if shelter_form.is_valid() and address_form.is_valid():
        shelter = Shelter.objects.filter(owner=request.user)
        address = ShelterAddress.objects.filter(shelter=shelter.first())
        shelter.update(**shelter_form.cleaned_data)
        address.update(**address_form.cleaned_data)
        return redirect('fido:shelter', pk=shelter.first().pk)
    context.update(forms=[shelter_form, address_form])
    return render(request, 'fido/form.html', context)


@login_required
@shelter_required
def remove_shelter(request):
    if request.method == 'POST':
        return remove_shelter_post(request)
    return remove_shelter_get(request)


def remove_shelter_get(request):
    shelter = request.user.shelter
    cat_count = Cat.objects.filter(shelter=shelter).count()
    dog_count = Dog.objects.filter(shelter=shelter).count()
    context = {'shelter': shelter, 'count': cat_count + dog_count}
    return render(request, 'fido/remove-shelter.html', context)


def remove_shelter_post(request):
    request.user.shelter.delete()
    return redirect('fido:homepage')


@login_required
@shelter_required
def manage_pets(request):
    page_obj = page_obj_all_pets(request, request.user.shelter)
    return render(request, 'fido/manage-pets.html', {'page_obj': page_obj})


def new_cat(request):
    context = {'title': 'New cat', 'headline': 'Cat Details'}
    return new_pet(request, CatForm, 'fido:cat', context)


def new_dog(request):
    context = {'title': 'New dog', 'headline': 'Dog Details'}
    return new_pet(request, DogForm, 'fido:dog', context)


@login_required
@shelter_required
def new_pet(request, form_class, pet_url, context):
    if request.method == 'POST':
        return new_pet_post(request, form_class, pet_url, context)
    return new_pet_get(request, form_class, context)


def new_pet_get(request, form_class, context):
    context.update(forms=[form_class()])
    return render(request, 'fido/form.html', context)


def new_pet_post(request, form_class, pet_url, context):
    form = form_class(request.POST, request.FILES)
    if form.is_valid():
        pet = form.save(commit=False)
        pet.shelter = request.user.shelter
        pet.save()
        return redirect(pet_url, pk=pet.pk)
    context.update(forms=[form])
    return render(request, 'fido/form.html', context)


def edit_cat(request, pk):
    context = {'title': 'Edit cat', 'headline': 'Cat Details'}
    return edit_pet(request, pk, Cat, EditCatForm, 'fido:cat', context)


def edit_dog(request, pk):
    context = {'title': 'Edit dog', 'headline': 'Dog Details'}
    return edit_pet(request, pk, Dog, EditDogForm, 'fido:dog', context)


@login_required
@shelter_required
def edit_pet(request, pk, model, form_class, pet_url, context):
    pet = get_object_or_404(model, pk=pk)
    if pet.shelter != request.user.shelter:
        raise PermissionDenied
    if request.method == 'POST':
        return edit_pet_post(request, pk, model, form_class, pet_url, context)
    return edit_pet_get(request, pet, form_class, context)


def edit_pet_get(request, pet, form_class, context):
    context.update(forms=[form_class(instance=pet)])
    return render(request, 'fido/form.html', context)


def edit_pet_post(request, pk, model, form_class, pet_url, context):
    form = form_class(request.POST, request.FILES)
    if form.is_valid():
        pet = model.objects.filter(pk=pk)
        pet.update(**form.cleaned_data)
        return redirect(pet_url, pk=pk)
    context.update(forms=[form])
    return render(request, 'fido/form.html', context)


def remove_cat(request, pk):
    return remove_pet(request, pk, Cat)


def remove_dog(request, pk):
    return remove_pet(request, pk, Dog)


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
