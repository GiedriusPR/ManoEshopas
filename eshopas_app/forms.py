from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Profile, Comment
from django import forms

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
        fields = ['img', 'home_address', 'city_town']  # Add home_address and city_town fields here

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            profile = self.instance
            self.fields['home_address'].initial = profile.home_address
            self.fields['city_town'].initial = profile.city_town
        except Profile.DoesNotExist:
            pass

    def save(self, commit=True):
        profile = super().save(commit=commit)
        profile.home_address = self.cleaned_data['home_address']
        profile.city_town = self.cleaned_data['city_town']
        profile.save()
        return profile

class ProductCommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
