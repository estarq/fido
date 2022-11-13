from django.forms import FileInput, ImageField, ModelForm

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
