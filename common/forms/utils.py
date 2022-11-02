from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe


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
