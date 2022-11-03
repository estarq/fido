from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from . import forms, views

app_name = 'accounts'

urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='accounts/login.html',
            authentication_form=forms.LoginForm,
            redirect_authenticated_user=True,
            next_page='fido:homepage',
        ),
        name='login',
    ),
    path('logout/', auth_views.LogoutView.as_view(next_page='fido:homepage'), name='logout'),
    path('privacy/', TemplateView.as_view(template_name='accounts/privacy.html'), name='privacy'),
    path('register/', views.register, name='register'),
    path('tos/', TemplateView.as_view(template_name='accounts/tos.html'), name='tos'),
]
