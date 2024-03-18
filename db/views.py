from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from .models import Item, Category, Audit, Order, ItemTag, Division
from .serializers import ItemSerializer, Item_Image, CategorySerializer, AuditSerializer, OrderSerializer, ItemTagSerializer, DivisionSerializer
import asyncio, datetime
from django.core.files.uploadedfile import InMemoryUploadedFile
from .google_updater import update_google_sheet
# Create your views here.
class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field = 'pk'
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        print(self)
        return Response(serializer.data)
    
   

class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

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
    serializer_class = ItemSerializer
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
        