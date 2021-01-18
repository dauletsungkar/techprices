"""This module describes model serializers"""
from rest_framework import serializers
from ..models import Product, Category, Price, Shop


class ShopSerializer(serializers.ModelSerializer):
    """Shop serializer"""
    class Meta:
        """This meta class specifies which model and which fields to serialize"""
        model = Shop
        fields = ['name']


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer"""
    class Meta:
        """This meta class specifies which model and which fields to serialize"""
        model = Category
        fields = ['id', 'name']


class PriceSerializer(serializers.ModelSerializer):
    """Price serializer"""
    shop = ShopSerializer(read_only=True)

    class Meta:
        """This meta class specifies which model and which fields to serialize"""
        model = Price
        fields = ['cost', 'shop']


class ProductSerializer(serializers.ModelSerializer):
    """Product serializer"""
    category = CategorySerializer(read_only=True)

    class Meta:
        """This meta class specifies which model and which fields to serialize"""
        model = Product
        fields = ['id', 'name', 'category']


class ProductWithPricesSerializer(serializers.ModelSerializer):
    """Product serializer for detail view to show all prices"""
    prices = PriceSerializer(many=True, read_only=True)

    class Meta:
        """This meta class specifies which model and which fields to serialize"""
        model = Product
        fields = ['name', 'prices']
