from django.contrib import admin
from django.db.models.fields.reverse_related import ManyToOneRel

from .models import Cat, Message, Dog, Shelter, ShelterAddress


class CustomModelAdmin(admin.ModelAdmin):
    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)
        self.list_display = [
            field.name for field in model._meta.get_fields()
            if not isinstance(field, ManyToOneRel)
        ]


for model in [Message, Cat, Dog, Shelter, ShelterAddress]:
    admin.site.register(model, CustomModelAdmin)
