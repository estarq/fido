from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from common.forms.models import StyledForm
from .models import User


class LoginForm(StyledForm, AuthenticationForm):
    pass


class NewUserForm(StyledForm, UserCreationForm):
    consent = forms.BooleanField()

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'consent']
