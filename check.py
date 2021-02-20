import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
import numpy as np
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('bert-base-nli-mean-tokens')
sentences = ['Ноутбук Apple MacBook Pro Touch Bar Retina 16 i7 9750H / 16ГБ / 512SSD / Radeon Pro 5300M 4ГБ / 16 / MacOS Catalina / (MVVJ2RU/A)']
sentence_embeddings = model.encode(sentences)
query = 'НОУТБУК APPLE MACBOOK PRO 16" SPACE GREY (MVVJ2)'
query_vec = model.encode([query])[0]
def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
for sent in sentences:
    sim = cosine(query_vec, model.encode([sent])[0])
    print("Sentence = ", sent, "; similarity = ", sim)
# import nltk
#     nltk.download('punkt')
#     import tensorflow_hub as hub
#     import numpy as np
#     from .models import Product, Hash, Price, Shop, Category
#
#     sentences = Hash.objects.all()
#
#     def cosine(u, v):
#         return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
#
#     module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
#     model = hub.load(module_url)
#
#     sentence_embeddings = model(sentences)
#     query_vec = model([name])[0]
#     shop_name = Shop.objects.get(pk=shop_id).get_name()
#     category_name = Category.objects.get(pk=category_id).get_name()
#     for sent in sentences:
#         sim = cosine(query_vec, model([sent])[0])
#         if sim >= 0.90:
#             Product.objects.create(name=name,category_id=category_id,hash_id=sent.id)
#             price = Price.objects.create(cost=cost,shop_id=shop_id,hash_id=sent.id)
#             send_price_to_bq.delay(cost=cost, date=price.get_date(), shop=shop_name, hash=sent.get_name())
#             f = False
#             break
#
#     if f:
#         hash = Hash.objects.create(name=name,category_id=category_id)
#         Product.objects.create(name=name, category_id=category_id, hash_id=hash.id)
#         price = Price.objects.create(cost=cost, shop_id=shop_id, hash_id=hash.id)
#         send_hash_to_bq.delay(name=name, category=category_name)
#         send_price_to_bq.delay(cost=cost, date=price.get_date(), shop=shop_name, hash=hash.get_name())
