from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class Signupform(UserCreationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder":"Enter Your Username"}))
    fname = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={"placeholder":"Enter Your First Name"}))
    lname = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={"placeholder":"Enter Your Last Name"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder":"Enter your Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Enter the Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm Your Password"}))

    class Meta:
        model = User
        fields = ('username', 'fname', 'lname', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder":"Email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))


