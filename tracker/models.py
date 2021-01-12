from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=500, unique=True)
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField(unique=True)

    def __str__(self):
        return self.name


class Price(models.Model):
    cost = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(
        Product, related_name='product_prices', on_delete=models.CASCADE)
    shop = models.ForeignKey(
        Shop, related_name='shop_prices', on_delete=models.CASCADE)

    def get_cost(self):
        return self.cost

    def __str__(self):
        return str(self.cost)


class Url(models.Model):
    url = models.URLField()
    category = models.ForeignKey(
        Category, related_name='category_urls', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, related_name='urls',
                             on_delete=models.CASCADE)

    def get_url(self):
        return self.url

    def get_category(self):
        return self.category.id

    def get_shop(self):
        return self.shop