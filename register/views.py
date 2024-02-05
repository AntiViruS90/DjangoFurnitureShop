from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import Group


# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name=form.cleaned_data.get('group'))
            user.groups.add(group)
        return redirect("/")
    else:
        form = RegisterForm()
    return render(request, "register/register.html", {"form": form})
