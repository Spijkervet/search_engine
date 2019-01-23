import pymongo
import numpy as np

from app.models import TfidfVector
from . import config

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["searchengine"]
crawler = db['crawler']
crawler.create_index([('title', 'text')])

arxiv = db['metadata']
index = db['index']

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

from bson.objectid import ObjectId
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity

from elasticsearch import Elasticsearch
es = Elasticsearch()


WORD_ID = '_id'
LIMIT = 25
tokenizer = RegexpTokenizer(r'\w+')

tfidf_vector = TfidfVector()

def process_query(query):
    q = tokenizer.tokenize(query)
    q = ' '.join([word for word in q if word not in stopwords.words('english')])
    return q

def create_arxiv_url(i):
    return 'https://arxiv.org/abs/' + i

def create_result(result):
    r = result['_source']
    r['id'] = result['_id']
    r['score'] = result['_score']
    r['url'] = create_arxiv_url(r['id'])
    return r

def elastic_search(query, categories):
    q = process_query(query)
    res = es.search(index="arxiv", body={"query": {"multi_match": { "query": query, "fields": ["title", "abstract", "authors.name"] }}})
    print("Got %d Hits:" % res['hits']['total'])
    r = []
    for hit in res['hits']['hits']:
        r.append(create_result(hit))
    return r

def convert_categories(chosen_cat, categories):
    new_cats = []
    for c in chosen_cat:
        new_cats.extend([v for k, v in config.config['categories'][c].items() if k in categories])
    return new_cats

def tokenize(t):
    t = tokenizer.tokenize(t)
    t = [word for word in t if word not in stopwords.words('english')]
    return ' '.join(t)

def search(query, categories):
    # get all sub category keys
    sub_cats = []
    for c in categories:
        sub_cats.extend([k for k, v in config.config['categories'][c].items()])

    q = tokenizer.tokenize(query)
    q = [word for word in q if word not in stopwords.words('english')]

    """
    OLD:
    results = index.find({ WORD_ID: { '$in': q } })
    docs = []
    for r in results:
        docs.extend([d for d in r['doc']])

    c = 0
    keys = []
    result_docs = []
    if sub_cats:
        result_docs = arxiv.find({ '_id': { '$in': docs  }, 'categories': { '$in': sub_cats }})
    else:
        result_docs = arxiv.find({ '_id': { '$in': docs } }, { '_id': True, 'abstract': True })

    result_abstracts = []
    for r in result_docs:
        keys.append(r['_id'])
        # a = tokenize(r['abstract'])
        result_abstracts.append(r['abstract'])

    if not result_docs:
    	return []
    r = vectorizer.fit_transform(result_abstracts)
    """

    q = [' '.join(q)]
    q = tfidf_vector.vectorizer.transform(q)
    cosine_similarities = cosine_similarity(q, tfidf_vector.X).flatten()
    best_doc_keys = cosine_similarities.argsort()[:-LIMIT:-1]
    doc_ids = np.asarray(tfidf_vector.ids)[best_doc_keys]
    ranking = []
    docs = arxiv.find({'_id': { '$in': list(doc_ids) }})
    for bc, (idx, doc) in zip(best_doc_keys, enumerate(docs)):
        ranking.append([doc, cosine_similarities[bc]])

    ranking = sorted(ranking, key=lambda x: x[1])
    # ranking = ranking[:LIMIT]
    final_ranking = []
    for r in ranking:
        d = {}
        d['doc'] = {
                'authors': r[0]['authors'],
                'date': r[0]['info']['created'],
                'description': r[0]['abstract'],
                'title': r[0]['title'],
                'categories': convert_categories(categories, r[0]['categories']),
                'url': 'https://arxiv.org/abs/' + r[0]['_id']
        }
        d['score'] = r[1]
        final_ranking.append(d)
    return final_ranking
