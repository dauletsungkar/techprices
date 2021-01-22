"""In this module we create our views"""
from rest_framework import generics, mixins
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Product, Category, Shop, Price, Hash
from .serializers import HashSerializer, HashWithPricesSerializer



class ProductListView(mixins.ListModelMixin, generics.GenericAPIView):
    """This class dispatches list of products"""
    queryset = Hash.objects.all()
    serializer_class = HashSerializer

    def get(self, request, *args, **kwargs):
        """Returns list of products"""
        return self.list(request, *args, **kwargs)


class ProductDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """This class dispatches detail of product by pk"""
    queryset = Hash.objects.all()
    serializer_class = HashWithPricesSerializer

    def get(self, request, *args, **kwargs):
        """Returns details of product"""
        return self.retrieve(request, *args, **kwargs)


class CategoryMinPrice(generics.GenericAPIView):
    """This class dispatches product with minimal price in category"""
    queryset = Category.objects.all()

    def get_minprice(self, hash):
        """Returns minimal price of product"""
        shops = Shop.objects.all()
        mn_price = hash.prices.latest('date').get_cost()
        for shop in shops:
            try:
                price = hash.prices.filter(
                    shop=shop).latest('date').get_cost()
                mn_price = min(mn_price, price)
            except Price.DoesNotExist:
                continue
        return mn_price

    def get(self, request, category_name):
        """Returns product details with minimal price in category"""
        category = get_object_or_404(Category, name=category_name)
        hashes = category.hashes.all()
        if len(hashes) > 0:
            mn_price = self.get_minprice(hashes[0])
            mn_product = hashes[0]
            for hash in hashes:
                price = self.get_minprice(hash)
                if price < mn_price:
                    mn_price = price
                    mn_product = hash
            serializer = HashWithPricesSerializer(mn_product)
            return Response(serializer.data)
        return Response()


class CategoryMaxPrice(generics.GenericAPIView):
    """This class dispatches product with maximal price in category"""
    queryset = Category.objects.all()

    def get_maxprice(self, hash):
        """Returns maximal price of product"""
        shops = Shop.objects.all()
        mx_price = hash.prices.latest('date').get_cost()
        for shop in shops:
            try:
                price = hash.prices.filter(
                    shop=shop).latest('date').get_cost()
                mx_price = max(mx_price, price)
            except Price.DoesNotExist:
                continue
        return mx_price

    def get(self, request, category_name):
        """Returns product details with maximal price in category"""
        category = get_object_or_404(Category, name=category_name)
        hashes = category.hashes.all()
        if len(hashes) > 0:
            mx_price = self.get_maxprice(hashes[0])
            mx_product = hashes[0]
            for hash in hashes:
                price = self.get_maxprice(hash)
                if price > mx_price:
                    mx_price = price
                    mx_product = hash
            serializer = HashWithPricesSerializer(mx_product)
            return Response(serializer.data)
        return Response()