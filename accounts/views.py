from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import ErrorAlerts, NewUserForm


def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST, error_class=ErrorAlerts)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('fido:homepage')
        return render(request, 'accounts/register.html', {'form': form})

    form = NewUserForm()
    return render(request, 'accounts/register.html', {'form': form})
