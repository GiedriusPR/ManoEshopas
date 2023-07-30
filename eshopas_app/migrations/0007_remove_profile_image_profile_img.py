# Generated by Django 4.2.3 on 2023-07-30 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshopas_app', '0006_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='image',
        ),
        migrations.AddField(
            model_name='profile',
            name='img',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
    ]
