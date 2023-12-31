# Generated by Django 4.1.10 on 2023-08-08 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0003_item_price_item_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlaggedItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('items', models.ManyToManyField(to='db.item')),
            ],
        ),
    ]
