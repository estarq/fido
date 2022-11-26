from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from common.forms.models import StyledForm, StyledModelForm
from .models import User


class NewUserForm(StyledModelForm, UserCreationForm):
    consent = forms.BooleanField()

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'consent']


class LoginForm(StyledForm, AuthenticationForm):
    pass
