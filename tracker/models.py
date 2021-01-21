"""This module describes database tables and relationships between them."""
from django.db import models


class Category(models.Model):
    """This model describes product categories"""
    name = models.CharField(max_length=100)

    def get_name(self):
        """Returns categories name"""
        return str(self.name)

    def __str__(self):
        return str(self.name)

class Hash(models.Model):
    name = models.CharField(max_length=500)
    category = models.ForeignKey(Category, related_name='hashes', on_delete=models.CASCADE)

    def get_name(self):
        """Returns name of hash"""
        return str(self.name)

class Product(models.Model):
    """This model describes products"""
    name = models.CharField(max_length=500, unique=True)
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    hash = models.ForeignKey(Hash, related_name='products', on_delete=models.CASCADE)

    def get_hash(self):
        """Returns products hash"""
        return self.hash

    def __str__(self):
        return str(self.name)


class Shop(models.Model):
    """This model describes the stores from which data will be used."""
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField(unique=True)

    def get_url(self):
        """Returns shops url"""
        return self.url

    def get_name(self):
        """Returns name of shop"""
        return self.name

    def __str__(self):
        return str(self.name)


class Price(models.Model):
    """This model describes the prices of products"""
    cost = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    hash = models.ForeignKey(
        Hash, related_name='prices', on_delete=models.CASCADE)
    shop = models.ForeignKey(
        Shop, related_name='shop_prices', on_delete=models.CASCADE)

    def get_cost(self):
        """Returns the cost"""
        return self.cost

    def get_date(self):
        """Returns date of price"""
        return self.date

    def __str__(self):
        return str(self.cost)


class Url(models.Model):
    """This model describes the pages of stores from which data will be collected"""
    url = models.URLField()
    category = models.ForeignKey(
        Category, related_name='category_urls', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, related_name='urls',
                             on_delete=models.CASCADE)

    def get_url(self):
        """Returns the url"""
        return self.url

    def get_category(self):
        """Returns the category"""
        return self.category

    def get_shop(self):
        """Returns the shop"""
        return self.shop
