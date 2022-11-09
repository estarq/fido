from django.forms import ModelForm

from common.forms.utils import ErrorAlerts
from .models import Contact, Shelter, ShelterAddress


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

    def __init__(self, *args, **kwargs):
        kwargs.update(error_class=ErrorAlerts)
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['message'].widget.attrs['rows'] = 4


class NewShelterForm(ModelForm):
    class Meta:
        model = Shelter
        fields = ['name', 'description', 'phone', 'email', 'website']

    def __init__(self, *args, **kwargs):
        kwargs.update(error_class=ErrorAlerts)
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['rows'] = 4


class NewShelterAddressForm(ModelForm):
    class Meta:
        model = ShelterAddress
        fields = ['state', 'city', 'street', 'zip_code']

    def __init__(self, *args, **kwargs):
        kwargs.update(error_class=ErrorAlerts)
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
