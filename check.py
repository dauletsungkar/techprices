import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
import numpy as np
import tensorflow_hub as hub
import numpy as np

sentences = ['Ноутбук Apple MacBook Pro Touch Bar Retina 16 i7 9750H / 16ГБ / 512SSD / Radeon Pro 5300M 4ГБ / 16 / MacOS Catalina / (MVVJ2RU/A)']
tokenized_sent = []
for s in sentences:
    tokenized_sent.append(word_tokenize(s.lower()))
tokenized_sent

def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(module_url)

sentence_embeddings = model(sentences)
query = 'НОУТБУК APPLE MACBOOK PRO 16" SPACE GREY (MVVJ2)'
query_vec = model([query])[0]

for sent in sentences:
    sim = cosine(query_vec, model([sent])[0])
    print("Sentence = ", sent, "; similarity = ", sim)