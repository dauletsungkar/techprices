from django.contrib import admin
from .models import Product, Category, Price, Shop, Url


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class PriceInline(admin.StackedInline):
    model = Price


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    inlines = [PriceInline]

class UrlInline(admin.StackedInline):
    model = Url

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']
    inlines = [UrlInline]

