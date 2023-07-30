from django.db import models
from PIL import Image
import logging
from tinymce import HTMLField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    type = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # increased max_digits
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    description = HTMLField()
    is_featured = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)
    sales_discount = models.FloatField(default=0.0)
    string = models.TextField(blank=True, null=True)
    discount = models.FloatField(default=0.0)

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


class Customer(models.Model):
    user = models.CharField(max_length=100)
    email = models.EmailField()
    product_id = models.IntegerField()

    def __str__(self):
        return self.user


class ProductOrder(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    string = models.TextField()

    def __str__(self):
        return f"Order ID: {self.order_id}, Customer: {self.customer}"


class Review(models.Model):
    status = models.IntegerField()
    name = models.CharField(max_length=100)
    order = models.ForeignKey(ProductOrder, on_delete=models.CASCADE, related_name='reviews', default=1)
    product_id = models.IntegerField()
    username = models.CharField(max_length=100)
    email = models.EmailField()
    review = models.TextField()


class Orders(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    string = models.CharField(max_length=100)
    integer = models.IntegerField()
    date = models.DateField()
    status_id = models.IntegerField()

    def __str__(self):
        return f"Order by {self.customer_id.user} - Status: {self.status_id}"


class User_login(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    product_id = models.IntegerField()

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True)
    img = models.ImageField(upload_to='profile_pics', default='default.jpg')
    thumbnail = ImageSpecField(source='img',
                               processors=[ResizeToFill(100, 50)],
                               format='JPEG',
                               options={'quality': 60})

    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()