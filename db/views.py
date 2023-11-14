from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from .models import Item, Category, Audit, Order, ItemTag, Division
from .serializers import ItemSerialier, Item_Image, CategorySerializer, AuditSerializer, OrderSerializer, ItemTagSerializer, DivisionSerializer
import asyncio, datetime
from django.core.files.uploadedfile import InMemoryUploadedFile
from .google_updater import update_google_sheet
# Create your views here.
class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerialier
    lookup_field = 'pk'
    def partial_update(self, request, *args, **kwargs):
        print("partial update called")
        instance = self.get_object()
        isAudit = request.data.get('is-audit')
        print("isAudit", isAudit)
        change_amount = request.data.get('change-amount', 0)
        change_min = request.data.get('change-min', 0)
        fullUpdate = request.data.get('full-update')
        print(request.data)
        if bool(fullUpdate):
            print('isfull update',fullUpdate)
            try:
                data = request.data
                instance.name = data['name']
                instance.quantity = data['quantity']
                instance.min_quantity = data['min_quantity']
                instance.category = Category.objects.get(name = data['category'])
                if instance.image != data['image']:
                    if isinstance(data['image'], InMemoryUploadedFile):
                        instance.image.save(data['image']) 
                
                instance.price = data['price']
                instance.url = data['url']
                instance.notes = data['notes']
                if data['cancelled']:
                    instance.cancelled = datetime.datetime.now()
                instance.save()
                return Response({"message": "successfully updated", 'status': HTTP_200_OK, "data":data, "item":str(instance)})
            except Exception as e:
                print(e)
                return Response({'status':HTTP_500_INTERNAL_SERVER_ERROR})
                pass
        try:
            change_amount = int(change_amount)
            change_min = int(change_min)
            isAudit =  isAudit == "True"
        except ValueError:
            return Response ({"error": "Invalid change_amount value"})
        

        print(bool(isAudit))
        instance.quantity += change_amount
        if isAudit:
            instance.quantity = change_amount
            instance.min_quantity = change_min
        if instance.quantity < 0:
            instance.quantity = 0
        instance.save()
        #asyncio.get_event_loop().create_task(update_google_sheet())
        print(instance.quantity)
        serializer = self.get_serializer(instance)
        
        return Response({"message":"successfully updated", "amount": instance.quantity, 'min': instance.min_quantity}, status=HTTP_200_OK)
    

class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerialier

class AuditList(generics.ListCreateAPIView):
    queryset = Audit.objects.all()
    serializer_class = AuditSerializer
class AuditDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Audit.objects.all()
    serializer_class = AuditSerializer
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
class ItemsByCategory(generics.ListCreateAPIView):
    serializer_class = ItemSerialier
    def get_queryset(self):
        category_name = self.kwargs["filter"]
        print(category_name)
        items = Item.objects.filter(category__name=category_name) 
        print([item for item in items])
        return items
class DepartmentList(generics.ListCreateAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
    
class ItemTagList(generics.ListCreateAPIView):
    queryset = ItemTag.objects.all()
    serializer_class = ItemTagSerializer
class PerformAudit(generics.RetrieveUpdateAPIView):
    queryset = Audit.objects.all()
    serializer_class = AuditSerializer
    def update(self, request, *args, **kwargs):
        division = self.kwargs["division_id"]
        req_items = self.kwargs["items"]
        req_items = []
        categories = Category.objects.filter(division=division)
        items  = []
        for cat in categories:
            items += Item.objects.filter(category=cat)
        