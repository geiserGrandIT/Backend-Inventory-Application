# Generated by Django 4.1.10 on 2023-08-08 22:25

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_division_alter_category_name_order_item_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
        migrations.AddField(
            model_name='item',
            name='url',
            field=models.CharField(default='', max_length=2048),
        ),
    ]
