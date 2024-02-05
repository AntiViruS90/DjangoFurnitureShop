
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    group = forms.ModelChoiceField(queryset=Group.objects.all(),
                                   required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "first_name", "last_name", "group"]
