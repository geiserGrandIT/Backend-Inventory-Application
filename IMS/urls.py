"""IMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from db.views import ItemTagList, ItemDetail, ItemList, AuditDetail, CategoryList, AuditList, OrderList, OrderDetail, ItemsByCategory, DepartmentList
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('items/',ItemList.as_view(), name="item-list"),
    path('items/<int:pk>/', ItemDetail.as_view(), name="item-detail"),
    path ('categories/', CategoryList.as_view(), name="category-list"),
    path('departments/', DepartmentList.as_view(), name='department-list'),
    path('audits/', AuditList.as_view(), name="audit-list"),
    path('audits/<int:pk>/', AuditDetail.as_view(), name="audit-detail"),
    path('orders/', OrderList.as_view(), name="order-list"),
    path('orders/<int:pk>/', OrderDetail.as_view(), name="order-detail"),
    path('categories/<str:filter>', ItemsByCategory.as_view(), name="item-category-list"),
    path('tags/', ItemTagList.as_view(), name='item-tag-list'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)