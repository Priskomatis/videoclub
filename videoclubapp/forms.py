from secrets import choice
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 

from .models import Profile


#Registration Form because we will create our own.

SEX_CHOICES = [('M', 'MALE'), ('F', 'FEMALE'),('O', 'OTHER')]

class RegisterForm(UserCreationForm):

    SEX_CHOICES = [('M', 'MALE'), ('F', 'FEMALE'),('O', 'OTHER')]
    GENRE_CHOICES = [('ACTION', 'ACTION'), ('DRAMA', 'DRAMA'),('MYSTERY', 'MYSTERY')]

    # fields we want to include and customize in our form
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput())

    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput)

    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput())

    email = forms.EmailField(required=True, widget=forms.TextInput())

    sex = forms.CharField(max_length=1, required=True, widget=forms.Select(choices=SEX_CHOICES))

    favGenre = forms.CharField(max_length=7, required=True, widget=forms.Select(choices=GENRE_CHOICES))

    password1 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())

    password2 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


#LOGIN FORM

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput())

    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']


#UPDATE USER AND PROFILE

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=50, required=True, widget=forms.TextInput())
    email = forms.CharField(max_length=50, required=True, widget=forms.TextInput())

    class Meta:
        model = User
        fields = ['username', 'email']

class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput())
    bio = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = User
        fields = ['avatar', 'bio']