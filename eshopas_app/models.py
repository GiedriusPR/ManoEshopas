import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
import logging
from django.shortcuts import get_object_or_404
from imagekit.models import ImageSpecField
from django.db.models.signals import post_save
from django.dispatch import receiver
from .image_processors import ResizeImageProcessor, ResizeToFill


class Category(models.Model):
    name = models.CharField(max_length=100)
    type = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(150, 200)], format='JPEG', options={'quality': 90})
    is_featured = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)
    sales_discount = models.FloatField(default=0.0)
    discount = models.FloatField(default=0.0)
    description = models.TextField(blank=True)
    favorites = models.ManyToManyField(User, related_name='favorites', blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        logger = logging.getLogger(__name__)

        try:
            img = Image.open(self.image.path)

            if img.height > 200 or img.width > 150:
                output_size = (150, 200)
                img.thumbnail(output_size)
                img.save(self.image.path)

                logger.info(f"Resized image for product {self.id} to {img.width}x{img.height}")

        except Exception as e:
            logger.exception(f"Failed to resize image for product {self.id}")

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def update_quantity(self, product_id, new_quantity):
        cart_item = get_object_or_404(CartItem, cart=self, product_id=product_id)
        cart_item.quantity = new_quantity
        cart_item.save()


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, default=None)

    def total_price(self):
        return self.product.price * self.quantity


class ProductComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    product_id = models.IntegerField()

    def __str__(self):
        return self.user.username


class ProductOrder(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    string = models.TextField()

    def __str__(self):
        return f"Order ID: {self.order_id}, Customer: {self.customer}"


class Review(models.Model):
    status = models.IntegerField()
    name = models.CharField(max_length=100)
    order = models.ForeignKey('ProductOrder', on_delete=models.CASCADE, related_name='reviews', default=None)
    product_id = models.IntegerField()
    username = models.CharField(max_length=100)
    email = models.EmailField()
    review = models.TextField()

    def save(self, *args, **kwargs):
        if not self.order:  # Check if the order instance is not provided
            # Set the default ProductOrder instance for reviews, assuming you have one with id=1
            self.order = ProductOrder.objects.get(pk=1)
        super().save(*args, **kwargs)


class Status(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    STATUS_CHOICES = (
        ('Paid-Waiting', 'Paid-Waiting'),
        ('Approved', 'Approved'),
        ('OnDelivery', 'On Delivery'),
        # Add other status choices as needed
    )

    status_type = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Paid-Waiting')

    def __str__(self):
        return self.status_type


class Order(models.Model):
    # Your other fields for the Order model
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        # Add more choices as needed
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    # Your other fields and methods for the Order model

class Orders(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, default=1, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    string = models.CharField(max_length=100)
    integer = models.IntegerField(null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        # Set the customer based on the authenticated user
        if not self.customer and self.user.is_authenticated:
            try:
                self.customer = Customer.objects.get(user=self.user)
            except Customer.DoesNotExist:
                # Handle the case where the customer is not found
                # You might want to create the customer here or display an error message
                pass

        super().save(*args, **kwargs)


class User_login(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    product_id = models.IntegerField()

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city_town = models.CharField(max_length=100, blank=True)
    home_address = models.CharField(max_length=255, blank=True)
    img = models.ImageField(upload_to='profile_pics', default='default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.product.name}"
