from datetime import datetime

class Log():

    def __init__(self, db):
        self.db = db

    def query_log(self, query):
        from .models import Query
        print("Logging", query, datetime.now())
        query = Query(query)
        self.db.session.add(query)
        self.db.session.commit()

    def click_log(self, idx, url):
        from .models import Click
        print("Log", idx, url)
        click = Click(idx, url)
        self.db.session.add(click)
        self.db.session.commit()

