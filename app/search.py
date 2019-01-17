import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["searchengine"]
crawler = db['crawler']
crawler.create_index([('title', 'text')])

arxiv = db['arxiv']
index = db['index']

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

from bson.objectid import ObjectId
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import pairwise_distances


def search(query):
    tokenizer = RegexpTokenizer(r'\w+')
    q = tokenizer.tokenize(query)
    q = list({word for word in q if word not in stopwords.words('english')})
    results = index.find({ 'word': { '$in': q } })

    docs = []
    for r in results:
        docs.extend([d for d in r['doc']])

    keys = []
    result_docs = []
    for d in docs:
        keys.append(d)
        result = arxiv.find_one({'_id': ObjectId(d)})
        result_docs.append(result['description'][0])

    vectorizer = TfidfVectorizer()

    r = vectorizer.fit_transform(result_docs)
    q = vectorizer.transform(q)
    sim = pairwise_distances(r, q)

    print(len(keys), len(sim))
    ranking = []
    for k, s in zip(keys, sim):
        doc = arxiv.find_one({'_id': ObjectId(k)})
        ranking.append([doc, s[0]])

    ranking = sorted(ranking, key=lambda x: x[1])
    print(ranking)
    final_ranking = []
    for r in ranking:
        d = {}
        d['doc'] = {
                'author': r[0]['author'],
                'date': r[0]['date'],
                'description': r[0]['description'][0],
                'comment': r[0]['description'][0],
                'title': r[0]['title'][0],
                'subject': r[0]['subject'],
                'type': r[0]['type'],
                'url': r[0]['url'][0]
        }
        d['score'] = r[1]
        final_ranking.append(d)
    return final_ranking
