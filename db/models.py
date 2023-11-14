from django.db import models
from imagefield import fields
from decimal import Decimal
import os
# Create your models here.
class Division(models.Model):
    name = models.CharField(max_length=1024)
    def __str__(self) -> str:
        return self.name
    
class Category(models.Model):
    name =  models.CharField(max_length=1024)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.name
    

class Item_Image(models.Model):
    image = models.ImageField(upload_to="item_images/")
    def __str(self) -> str:
        return os.path.basename(self.image.name)
class ItemTag(models.Model):
    name = models.CharField(max_length=1024)
    def __str__(self):
        return self.name
    
class Item(models.Model):
    name = models.CharField(max_length=1024)
    quantity = models.IntegerField()
    min_quantity = models.IntegerField(default=0, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ForeignKey(Item_Image, on_delete=models.CASCADE)
    last_update = models.DateTimeField()
    in_use = models.DateTimeField(blank=True)
    added = models.DateTimeField(auto_now=True)
    url = models.CharField(max_length=2048, default=str(""))
    price = models.DecimalField(max_digits=10,decimal_places=2, default=Decimal('0.00'))
    tags = models.ManyToManyField(ItemTag)
    notes = models.CharField(max_length=2048, blank=True, null=True)
    cancelled = models.DateField(blank=True, null=True)
    def __str__(self) -> str:
        return self.name

    
class Audit(models.Model):
    date = models.DateTimeField()
    items = models.ManyToManyField(Item)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return str(self.pk)
    
class Order(models.Model):
    items = models.ManyToManyField(Item)
    date =  models.DateTimeField()
    def __str__(self) -> str:
        return str(self.pk)
    
class FlaggedItems(models.Model):
    name= models.CharField(max_length=1024)
    items = models.ManyToManyField(Item)
    def __str__(self):
        return f"{self.name}: {', '.join(self.items)}"
