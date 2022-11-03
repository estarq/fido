from django.contrib import admin

from .models import Dog, Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Contact._meta.get_fields()]


admin.site.register(Contact, ContactAdmin)
admin.site.register(Dog)
