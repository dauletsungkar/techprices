"""This module configures the capabilities of the admin page"""
from django.contrib import admin
from .models import Product, Category, Price, Shop, Url


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Add a category model to the admin page"""
    list_display = ['name']


class PriceInline(admin.StackedInline):
    """Add a price model to the admin page"""
    model = Price


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Add a product model to the admin page"""
    list_display = ['name', 'category']
    inlines = [PriceInline]

class UrlInline(admin.StackedInline):
    """Add a category model to the admin page"""
    model = Url

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    """Add a category model to the admin page"""
    list_display = ['name', 'url']
    inlines = [UrlInline]
