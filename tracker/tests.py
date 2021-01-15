"""This module contains the tests of the tracker application"""
import json
import pytest
from django.urls import reverse
from .models import Product, Shop, Price, Category



@pytest.mark.django_db
def test_list_view(client):
    """Tests the view ProductList"""
    url = reverse('tracker:product_list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_detail_view(client):
    """Tests the view ProductDetail"""
    category = Category.objects.create(name='laptops')
    shop = Shop.objects.create(name='my_shop', url='http://myshop.kz/')
    product = Product.objects.create(name='Lenovo 8', category=category)
    Price.objects.create(cost=99999, product=product, shop=shop)
    url = reverse('tracker:product_detail', args =[1])
    response = client.get(url)
    assert response.status_code == 200
    content = json.loads(response.content)
    assert content['name'] == 'Lenovo 8'

@pytest.mark.django_db
def test_category_minprice_view(client):
    """Tests the view CategoryMinPrice"""
    category = Category.objects.create(name='laptops')
    shop = Shop.objects.create(name='my_shop', url='http://myshop.kz/')
    shop2 = Shop.objects.create(name='my_shop2', url='http://myshop2.kz/')
    product1 = Product.objects.create(name='Lenovo 8', category=category)
    Price.objects.create(cost=99999, product=product1, shop=shop)
    Price.objects.create(cost=109999, product=product1, shop=shop2)
    product2 = Product.objects.create(name='MacBook 15', category=category)
    Price.objects.create(cost=800000, product=product2, shop=shop)
    Price.objects.create(cost=789999, product=product2, shop=shop2)
    product3 = Product.objects.create(name='Acer Predator', category=category)
    Price.objects.create(cost=500000, product=product3, shop=shop)
    Price.objects.create(cost=515000, product=product3, shop=shop2)
    url = reverse('tracker:category_minprice', args=['laptops'])
    response = client.get(url)
    content = json.loads(response.content)
    assert response.status_code == 200
    assert content['name'] == 'Lenovo 8'

@pytest.mark.django_db
def test_category_maxprice_view(client):
    """Tests the view CategoryMaxPrice"""
    category = Category.objects.create(name='laptops')
    shop = Shop.objects.create(name='my_shop', url='http://myshop.kz/')
    shop2 = Shop.objects.create(name='my_shop2', url='http://myshop2.kz/')
    product1 = Product.objects.create(name='Lenovo 8', category=category)
    Price.objects.create(cost=99999, product=product1, shop=shop)
    Price.objects.create(cost=109999, product=product1, shop=shop2)
    product2 = Product.objects.create(name='MacBook 15', category=category)
    Price.objects.create(cost=800000, product=product2, shop=shop)
    Price.objects.create(cost=789999, product=product2, shop=shop2)
    product3 = Product.objects.create(name='Acer Predator', category=category)
    Price.objects.create(cost=500000, product=product3, shop=shop)
    Price.objects.create(cost=515000, product=product3, shop=shop2)
    url = reverse('tracker:category_maxprice', args=['laptops'])
    response = client.get(url)
    content = json.loads(response.content)
    assert response.status_code == 200
    assert content['name'] == 'MacBook 15'
