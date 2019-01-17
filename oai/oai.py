from sickle import Sickle
from db import db


ARXIV_URL = 'http://export.arxiv.org/oai2'
arxiv_coll = db['arxiv']

sickle = Sickle(ARXIV_URL)
sets = sickle.ListSets()

def get_records(s):
    return sickle.ListRecords(metadataPrefix="oai_dc", set=s.setSpec)


def insert_record(r):
    d = {
        "author": r['creator'],
        "date": r['date'],
        "title": r['title'],
        "subject": r['subject'],
        "type": r['type'],
        "description": r['description'],
        "url": r['identifier']
    }

    x = arxiv_coll.insert_one(d)
    print(x)

for s in sets:
    records = get_records(s)
    for r in records:
        m = r.metadata
        insert_record(m)
    break
