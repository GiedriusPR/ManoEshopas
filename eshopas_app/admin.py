from django.contrib import admin
from .models import Category, Product, Customer, ProductOrder, Review, Orders, User_login

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_featured', 'category', 'stock', 'image', 'description']

    def image_tag(self, obj):
        return f'<img src="{obj.thumbnail.url}" width="100" height="150" />'
    image_tag.short_description = 'Thumbnail'

    fields = ['name', 'price', 'is_featured', 'category', 'stock', 'image', 'description']


# Register the rest of the models
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Orders)
admin.site.register(ProductOrder)
admin.site.register(Review)
admin.site.register(User_login)
