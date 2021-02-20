"""This module stores all tasks of the tracker application"""
from celery import shared_task


@shared_task
def update_data():
    """This periodic task collects data from all stores and updates the database"""
    from .logic import Sulpak, BelyiVeter, TechnoDom, Mechta
    shops = [BelyiVeter(), Mechta(), Sulpak(), TechnoDom()]
    for shop in shops:
        shop.get_data()



@shared_task
def match(name, category_id, cost, shop_id):
    """Match products by name"""
    import math
    import re
    from collections import Counter
    from .models import Product, Hash, Price, Shop, Category
    WORD = re.compile(r"\w+")

    def get_cosine(vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
        sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

    def text_to_vector(text):
        words = WORD.findall(text)
        return Counter(words)

    f = True
    shop_name = Shop.objects.get(pk=shop_id).get_name()
    category_name = Category.objects.get(pk=category_id).get_name()
    vector1 = text_to_vector(name)
    sentences = Hash.objects.all()
    for sent in sentences:
        vector2 = text_to_vector(sent.get_name())
        sim = get_cosine(vector1, vector2)
        if sim >= 0.90:
            Product.objects.create(name=name,category_id=category_id,hash_id=sent.id)
            price = Price.objects.create(cost=cost,shop_id=shop_id,hash_id=sent.id)
            f = False
            break
    if f:
        hash = Hash.objects.create(name=name,category_id=category_id)
        Product.objects.create(name=name, category_id=category_id, hash_id=hash.id)
        Price.objects.create(cost=cost, shop_id=shop_id, hash_id=hash.id)