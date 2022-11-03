from django.urls import path
from django.views.generic import TemplateView

from fido import views

app_name = 'fido'

urlpatterns = [
    path('', TemplateView.as_view(template_name='fido/index.html'), name='homepage'),
    path('contact/', views.contact, name='contact'),
    path('for-shelters/', TemplateView.as_view(template_name='fido/for-shelters.html'), name='for-shelters'),
]
