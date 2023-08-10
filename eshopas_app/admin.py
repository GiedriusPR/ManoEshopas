from django.contrib import admin
from .models import Category, Product, Customer, Review, Orders, User_login, Status, ShippingAddress
from PIL import Image
from django.utils.html import format_html

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_featured', 'category', 'stock', 'description']
    list_display_links = ['name']
    search_fields = ['name', 'description']
    list_filter = ['is_featured', 'category', 'stock']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'date_posted', 'approved')
    list_filter = ('approved')
    search_fields = ('user__username', 'product__title')


    # def image_tag(self, obj):
    #     try:
    #         # img = Image.open(obj.thumbnail.path)
    #         img.thumbnail((150, 200), Image.LANCZOS)  # Use Image.LANCZOS for resizing
    #         return format_html('<img src="{}" />', img.url)
    #     except:
    #         return "Image not available"
    #
    # image_tag.short_description = 'Thumbnail'



# Register the rest of the models
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Orders)
admin.site.register(Review)
admin.site.register(User_login)
admin.site.register(Status)