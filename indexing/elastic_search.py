from db import db
from elasticsearch import Elasticsearch
es = Elasticsearch()

"""
def import():
    arxiv_coll = db['metadata']
    cursor = arxiv_coll.find({})

    c = 0
    for doc in cursor:
        i = doc['_id']
        print("ADDED", i)
        doc.pop('_id', None)
        res = es.index(index="arxiv", doc_type='article', id=i, body=doc)
        c += 1
        if c > 1000:
            break

    es.indices.refresh(index="arxiv")
"""

res = es.search(index="arxiv", body={"query": {"match": { "abstract": "test" }}})
print("Got %d Hits:" % res['hits']['total'])

