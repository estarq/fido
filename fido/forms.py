from django.forms import ChoiceField, FileInput, ImageField, ModelForm

from common.constants import US_STATES
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


class EditPetForm(ModelForm):
    photo = ImageField(required=False, widget=FileInput)

    def clean(self):
        if not self.cleaned_data['photo']:
            self.cleaned_data.pop('photo')
        super().clean()


class EditCatForm(EditPetForm, CatForm):
    pass


class EditDogForm(EditPetForm, DogForm):
    pass


class SearchPetsForm(StyledForm):
    shelter__shelteraddress__state = ChoiceField(choices=US_STATES, label='State')

    class Meta:
        fields = ['breed', 'age', 'sex', 'shelter__shelteraddress__state']


class SearchCatsForm(SearchPetsForm, ModelForm):
    class Meta(SearchPetsForm.Meta):
        model = Cat


class SearchDogsForm(SearchPetsForm, ModelForm):
    class Meta(SearchPetsForm.Meta):
        model = Dog
