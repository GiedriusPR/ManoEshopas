from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tinymce import TinyMCE
from django import forms
from .models import Product


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class CartForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())



class ProductForm(forms.ModelForm):
    description = forms.CharField(widget=TinyMCE())

    class Meta:
        model = Product
        fields = '__all__' # or list the fields you want