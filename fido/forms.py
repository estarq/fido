from django import forms

from common.constants import US_STATES
from common.forms.models import StyledModelForm
from .models import Message, Cat, Dog, Shelter, ShelterAddress


class ContactForm(StyledModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'message']


class SearchPetsForm(StyledModelForm):
    shelter__shelteraddress__state = forms.ChoiceField(choices=US_STATES, label='State')

    class Meta:
        fields = ['breed', 'age', 'sex', 'shelter__shelteraddress__state']


class SearchCatsForm(SearchPetsForm):
    class Meta(SearchPetsForm.Meta):
        model = Cat


class SearchDogsForm(SearchPetsForm):
    class Meta(SearchPetsForm.Meta):
        model = Dog


class ShelterForm(StyledModelForm):
    class Meta:
        model = Shelter
        fields = ['name', 'description', 'phone', 'email', 'website']


class ShelterAddressForm(StyledModelForm):
    class Meta:
        model = ShelterAddress
        fields = ['street', 'city', 'zip_code', 'state']


class PetForm(StyledModelForm):
    class Meta:
        fields = ['name', 'description', 'photo', 'breed', 'age', 'sex']


class CatForm(PetForm):
    class Meta(PetForm.Meta):
        model = Cat


class DogForm(PetForm):
    class Meta(PetForm.Meta):
        model = Dog


class EditPetForm(StyledModelForm):
    photo = forms.ImageField(required=False, widget=forms.FileInput)

    def clean(self):
        if not self.cleaned_data['photo']:
            self.cleaned_data.pop('photo')
        super().clean()


class EditCatForm(EditPetForm, CatForm):
    pass


class EditDogForm(EditPetForm, DogForm):
    pass
