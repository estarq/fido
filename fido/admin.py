from django.contrib import admin

from .models import Dog, Contact, Shelter, ShelterAddress


class ContactAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Contact._meta.get_fields()]


class ShelterAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Shelter._meta.get_fields()]


class ShelterAddressAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ShelterAddress._meta.get_fields()]


admin.site.register(Contact, ContactAdmin)
admin.site.register(Dog)
admin.site.register(Shelter, ShelterAdmin)
admin.site.register(ShelterAddress, ShelterAddressAdmin)
