import tensorflow_hub as hub
import numpy as np
module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(module_url)
sentences = ['Ноутбук Apple MacBook Pro Touch Bar Retina 16 i7 9750H / 16ГБ / 512SSD / Radeon Pro 5300M 4ГБ / 16 / MacOS Catalina / (MVVJ2RU/A)']
sentence_embeddings = model(sentences)
query = 'НОУТБУК APPLE MACBOOK PRO 16" SPACE GREY (MVVJ2)'
query_vec = model([query])[0]

def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

for sent in sentences:
  sim = cosine(query_vec, model([sent])[0])
  print("Sentence = ", sent, "; similarity = ", sim)