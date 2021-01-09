from django.urls import path, include
from . import views

app_name = 'courses'

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<pk>/', views.ProductDetailView.as_view(), name='product_detail'),
]
