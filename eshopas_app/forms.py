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
    home_address = forms.CharField(max_length=255, required=False)
    city_town = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            profile = self.instance.profile
            self.fields['home_address'].initial = profile.home_address
            self.fields['city_town'].initial = profile.city_town
        except Profile.DoesNotExist:
            pass

    def save(self, commit=True):
        user = super().save(commit=commit)
        try:
            profile = user.profile
            profile.home_address = self.cleaned_data['home_address']
            profile.city_town = self.cleaned_data['city_town']
            profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=user, home_address=self.cleaned_data['home_address'],
                                   city_town=self.cleaned_data['city_town'])
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['img']


class ProductCommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))