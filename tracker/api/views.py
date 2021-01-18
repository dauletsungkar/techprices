"""In this module we create our views"""
from rest_framework import generics, mixins
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Product, Category, Shop, Price
from .serializers import ProductSerializer, ProductWithPricesSerializer



class ProductListView(mixins.ListModelMixin, generics.GenericAPIView):
    """This class dispatches list of products"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        """Returns list of products"""
        return self.list(request, *args, **kwargs)


class ProductDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """This class dispatches detail of product by pk"""
    queryset = Product.objects.all()
    serializer_class = ProductWithPricesSerializer

    def get(self, request, *args, **kwargs):
        """Returns details of product"""
        return self.retrieve(request, *args, **kwargs)


class CategoryMinPrice(generics.GenericAPIView):
    """This class dispatches product with minimal price in category"""
    queryset = Category.objects.all()

    def get_minprice(self, product):
        """Returns minimal price of product"""
        shops = Shop.objects.all()
        mn_price = product.product_prices.latest('date').get_cost()
        for shop in shops:
            try:
                price = product.prices.filter(
                    shop=shop).latest('date').get_cost()
                mn_price = min(mn_price, price)
            except Price.DoesNotExist:
                continue
        return mn_price

    def get(self, request, category_name):
        """Returns product details with minimal price in category"""
        category = get_object_or_404(Category, name=category_name)
        products = category.products.all()
        if len(products) > 0:
            mn_price = self.get_minprice(products[0])
            mn_product = products[0]
            for product in products:
                price = self.get_minprice(product)
                if price < mn_price:
                    mn_price = price
                    mn_product = product
            serializer = ProductWithPricesSerializer(mn_product)
            return Response(serializer.data)
        return Response()


class CategoryMaxPrice(generics.GenericAPIView):
    """This class dispatches product with maximal price in category"""
    queryset = Category.objects.all()

    def get_maxprice(self, product):
        """Returns maximal price of product"""
        shops = Shop.objects.all()
        mx_price = product.prices.latest('date').get_cost()
        for shop in shops:
            try:
                price = product.product_prices.filter(
                    shop=shop).latest('date').get_cost()
                mx_price = max(mx_price, price)
            except Price.DoesNotExist:
                continue
        return mx_price

    def get(self, request, category_name):
        """Returns product details with maximal price in category"""
        category = get_object_or_404(Category, name=category_name)
        products = category.products.all()
        if len(products) > 0:
            mx_price = self.get_maxprice(products[0])
            mx_product = products[0]
            for product in products:
                price = self.get_maxprice(product)
                if price > mx_price:
                    mx_price = price
                    mx_product = product
            serializer = ProductWithPricesSerializer(mx_product)
            return Response(serializer.data)
        return Response()