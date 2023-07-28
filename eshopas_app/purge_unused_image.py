from django.core.management.base import BaseCommand
from .models import Product

class Command(BaseCommand):
    help = 'Purge unused images'

    def handle(self, *args, **options):
        # Your logic to purge unused images goes here
        # For example, you can use the ResizeImageProcessor to check for unused images
        # and delete them from the storage.

        # Sample code to get you started (assuming you have a 'deleted' field in your model)
        unused_products = Product.objects.filter(deleted=True)
        for product in unused_products:
            product.image.delete()
