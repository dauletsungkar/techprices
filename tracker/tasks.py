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
def send_hash_to_bq(name, category):
    """Add new row to products table in bigquery"""
    from google.cloud import bigquery
    client = bigquery.Client()
    rows_to_insert = [
        {u"name": name, u"category": category}
    ]
    errors = client.insert_rows_json('techprices.tracker.hashes', rows_to_insert)
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))

@shared_task
def send_price_to_bq(cost, date, shop, hash):
    """Add new row to prices table in bigquery"""
    from google.cloud import bigquery
    client = bigquery.Client()
    rows_to_insert = [
        {u"cost": cost, u"date": date, u"shop": shop, u"hash": hash}
    ]
    errors = client.insert_rows_json('techprices.tracker.prices', rows_to_insert)
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))


@shared_task
def match(name, category_id, cost, shop_id):
    """Match products by name"""
    import tensorflow_hub as hub
    import numpy as np
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    model = hub.load(module_url)
    # sentences = [
    #     'Ноутбук Apple MacBook Pro Touch Bar Retina 16 i7 9750H / 16ГБ / 512SSD / Radeon Pro 5300M 4ГБ / 16 / MacOS Catalina / (MVVJ2RU/A)']
    # sentence_embeddings = model(sentences)
    # query = 'НОУТБУК APPLE MACBOOK PRO 16" SPACE GREY (MVVJ2)'
    # query_vec = model([query])[0]
    #
    # def cosine(u, v):
    #     return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
    #
    # for sent in sentences:
    #     sim = cosine(query_vec, model([sent])[0])
    #     print("Sentence = ", sent, "; similarity = ", sim)
    # import tensorflow as tf
    # import tensorflow_hub as hub
    # import numpy as np
    # from .models import Hash, Product, Price, Shop, Category
    # module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    # model = hub.load(module_url)
    # hashes = Hash.objects.all()
    # sentences = [hash.get_name() for hash in hashes]
    # sentence_embeddings = model(sentences)
    # query = name
    # query_vec = model([query])[0]
    #
    # def cosine(u, v):
    #     return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
    #
    # f = True
    # shop_name = Shop.objects.get(pk=shop_id).get_name()
    # category_name = Category.objects.get(pk=category_id).get_name()
    # for sent in sentences:
    #     sim = cosine(query_vec, model([sent.get_name()])[0])
    #     if sim >= 0.90:
    #         Product.objects.create(name=name,category_id=category_id,hash_id=sent.id)
    #         price = Price.objects.create(cost=cost,shop_id=shop_id,hash_id=sent.id)
    #         send_price_to_bq.delay(cost=cost, date=price.get_date(), shop=shop_name, product=sent.get_name())
    #         f = False
    #         break
    # if f:
    #     hash = Hash.objects.create(name=name,category_id=category_id)
    #     Product.objects.create(name=name, category_id=category_id, hash_id=hash.id)
    #     price = Price.objects.create(cost=cost, shop_id=shop_id, hash_id=hash.id)
    #     send_hash_to_bq.delay(name=name, category=category_name)
    #     send_price_to_bq.delay(cost=cost, date=price.get_date(), shop=shop_name, product=hash.get_name())
