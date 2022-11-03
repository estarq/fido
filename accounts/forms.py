from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from common.forms.utils import ErrorAlerts
from .models import User


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        kwargs.update(error_class=ErrorAlerts)
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class NewUserForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    consent = forms.BooleanField()

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'consent']

    def __init__(self, *args, **kwargs):
        kwargs.update(error_class=ErrorAlerts)
        super().__init__(*args, **kwargs)
        for field in ['email', 'password1', 'password2']:
            self.fields[field].widget.attrs['class'] = 'form-control'
