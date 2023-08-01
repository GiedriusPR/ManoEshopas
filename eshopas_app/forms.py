from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product
from django import forms
from .models import Profile


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class CartForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['img']
