from textwrap import wrap

from django import template

register = template.Library()


@register.filter
def format_phone_number(number):
    digits = ''.join(filter(str.isdigit, number))
    return ' '.join(wrap(digits, 3))


@register.filter
def get_pet_url(pet, action=''):
    class_name = str.lower(pet.__class__.__name__)
    return f'fido:{action}-{class_name}' if action else f'fido:{class_name}'
