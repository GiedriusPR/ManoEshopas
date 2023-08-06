# Generated by Django 4.2.3 on 2023-08-06 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshopas_app', '0002_alter_orders_integer'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='status_type',
            field=models.CharField(choices=[('Paid-Waiting', 'Paid-Waiting'), ('Approved', 'Approved'), ('OnDelivery', 'On Delivery')], default='Paid-Waiting', max_length=20),
        ),
    ]