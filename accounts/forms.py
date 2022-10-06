from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe

from .models import User


class NewUserForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    consent = forms.BooleanField()

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'consent']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['email', 'password1', 'password2']:
            self.fields[field].widget.attrs['class'] = 'form-control'


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        kwargs.update(error_class=ErrorAlerts)
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class ErrorAlerts(ErrorList):
    def __str__(self):
        return '' if not self else mark_safe(
            ''.join(
                '<div class="alert alert-danger mt-n2" role="alert">'
                f'<div class="alert-inner--text" style="margin-left: -0.75rem !important">{err}</div>'
                '</div>'
                for err in self
            )
        )
