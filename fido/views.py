from django.shortcuts import render

from .forms import ContactForm


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            form = ContactForm()
            return render(request, 'fido/contact.html', {'form': form, 'sent': True})
        return render(request, 'fido/contact.html', {'form': form, 'sent': False})

    form = ContactForm()
    return render(request, 'fido/contact.html', {'form': form})
