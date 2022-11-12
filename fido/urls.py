from django.urls import path
from django.views.generic import TemplateView
from .models import Cat, Dog

from fido import views

app_name = 'fido'

urlpatterns = [
    path('', TemplateView.as_view(template_name='fido/index.html'), name='homepage'),
    path('contact/', views.contact, name='contact'),
    path('cat/<int:pk>/', views.pet, name='cat', kwargs={'model': Cat}),
    path('dog/<int:pk>/', views.pet, name='dog', kwargs={'model': Dog}),
    path('for-shelters/', TemplateView.as_view(template_name='fido/for-shelters.html'), name='for-shelters'),
    path('shelter/<int:pk>/', views.shelter_page, name='shelter'),
    path('shelter/edit/', views.edit_shelter, name='edit-shelter'),
    path('shelter/new/', views.new_shelter, name='new-shelter'),
]
