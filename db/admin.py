from django.contrib import admin
from .models import Item, Category, Audit, Order, Division, ItemTag, Item_Image
# Register your models here.
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Audit)
admin.site.register(Order)
admin.site.register(Division)
admin.site.register(ItemTag)
admin.site.register(Item_Image)