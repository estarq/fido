from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import NewUserForm


def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('fido:new-shelter')
        return render(request, 'accounts/register.html', {'form': form})

    form = NewUserForm()
    return render(request, 'accounts/register.html', {'form': form})
