from django.forms import ModelForm
from django import forms ## a form class describes a form and determines how it works and appears.
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Log, Profile

class LogForm(ModelForm):
    class Meta:
        model = Log
        fields = ['date','order']

class UserSignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1', 'password2']

##forms.ModelForm automatically created form from models, to also avoid duplications
## Nxt configuarion will be to manually create a form by using forms.form
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']