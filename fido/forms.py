from django.forms import ModelForm

from common.forms.models import StyledForm
from .models import Contact, Cat, Dog, Shelter, ShelterAddress


class ContactForm(StyledForm, ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class ShelterForm(StyledForm, ModelForm):
    class Meta:
        model = Shelter
        exclude = ['owner']


class ShelterAddressForm(StyledForm, ModelForm):
    class Meta:
        model = ShelterAddress
        exclude = ['shelter']


class CatForm(StyledForm, ModelForm):
    class Meta:
        model = Cat
        exclude = ['shelter']


class DogForm(StyledForm, ModelForm):
    class Meta:
        model = Dog
        exclude = ['shelter']
