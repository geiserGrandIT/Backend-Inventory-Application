from .models import Item, Category, Audit, Order, Item_Image, ItemTag, Division
from rest_framework.serializers import ModelSerializer

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
    pass
class ImageSerializer(ModelSerializer):
    class Meta:
        model = Item_Image
        fields = "__all__"

class ItemTagSerializer(ModelSerializer):
    class Meta:
        model = ItemTag
        fields = "__all__"
        
class ItemSerializer(ModelSerializer):
    category = CategorySerializer(many=False)
    image = ImageSerializer(many=False)
    tags = ItemTagSerializer(many=True)
    
    class Meta:
        model = Item
        fields = "__all__"
        partial = True





class AuditSerializer(ModelSerializer):
    items = ItemSerializer(many=True)
    class Meta:
        model = Audit
        fields = "__all__"
    pass
class OrderSerializer(ModelSerializer):
    items = ItemSerializer(many=True)
    class Meta:
        model = Order
        fields = "__all__"
class DivisionSerializer(ModelSerializer):
    class Meta:
        model = Division
        fields = "__all__"