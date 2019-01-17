from db import db
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import pymongo

tokenizer = RegexpTokenizer(r'\w+')
index = db["index"]
index.create_index([("word", pymongo.TEXT)], unique=True)

def add_index(tokens, doc):
    try:
        x = index.insert_many([{ 'word': t } for t in tokens], ordered=False)
    except Exception as e:
        pass
    index.update_many({'word': {'$in': list(tokens) }}, {'$push': {'doc': doc}}, upsert=True)

arxiv_coll = db['metadata']
cursor = arxiv_coll.find({})
for document in cursor:
    doc = document['_id']
    desc = document['abstract']
    tokens = [t.lower() for t in tokenizer.tokenize(desc)]
    tokens = {word for word in tokens if word not in stopwords.words('english')}
    add_index(tokens, doc)
