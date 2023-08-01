from django.contrib import admin
from .forms import ProductForm
from .models import Category, Product, Customer, ProductOrder, Review, Orders, User_login
from django import forms

class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea,
        required=True,
    )

    class Meta:
        model = Product
        fields = '__all__'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ['name', 'price', 'is_featured', 'category', 'stock', 'image', 'description']

    def get_html_content(self, obj):
        return obj.description

    get_html_content.short_description = 'HTML Field'

# Register the rest of the models
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Orders)
admin.site.register(ProductOrder)
admin.site.register(Review)
admin.site.register(User_login)
