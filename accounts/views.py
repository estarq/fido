from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import NewUserForm


def register(request):
    if request.user.is_authenticated:
        return redirect('fido:new-shelter')
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            login(request, user=form.save())
            return redirect('fido:new-shelter')
        return render(request, 'accounts/register.html', {'form': form})
    return render(request, 'accounts/register.html', {'form': NewUserForm()})
