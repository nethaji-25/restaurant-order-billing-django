from django import forms
from .models import Empdata
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class Userform(forms.ModelForm):
    class Meta:
        model= Empdata
        fields="__all__"



class Registerform(UserCreationForm):
    class Meta:
        model=User
        fields=["username","password1","password2"]
