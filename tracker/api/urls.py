"""In this module, we map views to urls to call them"""
from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = 'tracker'

urlpatterns = [
    path('products/', cache_page(60 * 15)
         (views.ProductListView.as_view()), name='product_list'),
    path('products/<int:pk>/', cache_page(60 * 15)
         (views.ProductDetailView.as_view()), name='product_detail'),
    path('<category_name>/minprice/', cache_page(60 * 15)
         (views.CategoryMinPrice.as_view()), name='category_minprice'),
    path('<category_name>/maxprice/', cache_page(60 * 15)
         (views.CategoryMaxPrice.as_view()), name='category_maxprice'),
]
