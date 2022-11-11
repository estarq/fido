from django.contrib import admin
from django.db.models.fields.reverse_related import ManyToOneRel

from .models import Cat, Contact, Dog, Shelter, ShelterAddress


class DynamicModelAdmin(admin.ModelAdmin):
    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)
        self.list_display = [
            field.name for field in model._meta.get_fields()
            if not isinstance(field, ManyToOneRel)
        ]


admin.site.register(Cat, DynamicModelAdmin)
admin.site.register(Contact, DynamicModelAdmin)
admin.site.register(Dog, DynamicModelAdmin)
admin.site.register(Shelter, DynamicModelAdmin)
admin.site.register(ShelterAddress, DynamicModelAdmin)
