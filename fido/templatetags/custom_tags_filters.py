from textwrap import wrap

from django import template

register = template.Library()


@register.filter
def format_phone_number(number):
    digits = ''.join(filter(str.isdigit, number))
    return ' '.join(wrap(digits, 3))
