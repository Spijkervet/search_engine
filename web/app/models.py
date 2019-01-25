from flask_login import UserMixin
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import db, bcrypt
import os
import pickle

class TfidfVector():

    vec = None
    ids = None

    def __init__(self):
        pass
        """
        VECTOR_FILE = 'vectors.p'
        if os.path.isfile(VECTOR_FILE):
            handle = open(VECTOR_FILE, 'rb')
            ds = pickle.load(handle)
            self.ids = ds['ids']
            self.X = ds['X']
            self.vectorizer = ds['vectorizer']
            handle.close()
            print("LOADED VECTORS:")
        """
engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class User(Base):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, email=None, password=None):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)


    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


    def logout(self):
        self.authenticated = False
        db.session.commit()


    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

class Query(Base):
    __tablename__ = 'queries'

    id = db.Column(db.Integer, primary_key=True)
    # session = db.Column(db.String(128))
    query = db.Column(db.String(256))
    created = db.Column('datetime', db.DateTime, default=db.func.now())

    def __init__(self, query):
        self.query = query


class Click(Base):
    __tablename__ = 'clicks'

    id = db.Column(db.Integer, primary_key=True)
    # session = db.Column(db.String(128))
    query_idx = db.Column(db.Integer)
    url = db.Column(db.String(256))

    def __init__(self, query_idx, url):
        self.query_idx = query_idx
        self.url = url

Base.metadata.create_all(bind=engine)
