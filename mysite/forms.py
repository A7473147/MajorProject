from django import forms
from django.forms.forms import Form
from . import views

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.PasswordInput()
    