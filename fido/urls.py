from django.urls import path
from django.views.generic import TemplateView

from fido import views

app_name = 'fido'

urlpatterns = [
    path('', TemplateView.as_view(template_name='fido/index.html'), name='homepage'),
    path('for-shelters/', TemplateView.as_view(template_name='fido/for-shelters.html'), name='for-shelters'),
    path('contact/', views.contact, name='contact'),
    path('cat/<int:pk>/', views.cat_page, name='cat'),
    path('dog/<int:pk>/', views.dog_page, name='dog'),
    path('search/cats/', views.search_cats, name='search-cats'),
    path('search/dogs/', views.search_dogs, name='search-dogs'),
    path('search/cats/<slug:breed>/<slug:age>/<slug:sex>/<slug:shelter__shelteraddress__state>/',
         views.search_cats_params),
    path('search/dogs/<slug:breed>/<slug:age>/<slug:sex>/<slug:shelter__shelteraddress__state>/',
         views.search_dogs_params),
    path('shelter/<int:pk>/', views.shelter_page, name='shelter'),
    path('shelter/new/', views.new_shelter, name='new-shelter'),
    path('shelter/edit/', views.edit_shelter, name='edit-shelter'),
    path('shelter/remove/', views.remove_shelter, name='remove-shelter'),
    path('shelter/pets/', views.manage_pets, name='manage-pets'),
    path('shelter/cat/new/', views.new_cat, name='new-cat'),
    path('shelter/dog/new/', views.new_dog, name='new-dog'),
    path('shelter/cat/<int:pk>/edit/', views.edit_cat, name='edit-cat'),
    path('shelter/dog/<int:pk>/edit/', views.edit_dog, name='edit-dog'),
    path('shelter/cat/<int:pk>/remove/', views.remove_cat, name='remove-cat'),
    path('shelter/dog/<int:pk>/remove/', views.remove_dog, name='remove-dog'),
]
