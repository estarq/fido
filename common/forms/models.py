from django import forms
from django.forms.widgets import Textarea

from .utils import ErrorAlerts


class StyledForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.update(error_class=ErrorAlerts)
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            if isinstance(self.fields[field].widget, Textarea):
                self.fields[field].widget.attrs['rows'] = 4
