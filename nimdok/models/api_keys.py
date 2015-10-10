from sqlalchemy import Column, String
from .shared import declarative_base, db


class ApiKeyModel(declarative_base):
    __tablename__ = 'api_keys'

    def __init__(self, name, key):
        self.name = name
        self.key = key

    domain = Column(String, unique=True, primary_key=True)
    key = Column(String)

    @staticmethod
    def list():
        keys = ApiKeyModel.query.all()
        out = {}

        for k in keys:
            out[k.name] = k.key

        return out

    @staticmethod
    def get(name):
        return ApiKeyModel.query \
                   .filter_by(domain=name.upper()) \
                   .first()

    @staticmethod
    def set(name, key):
        try:
            ApiKeyModel.query.filter_by(name=name.upper()).remove()
            db.session.commit()
        finally:
            db.session.add(ApiKeyModel(name.upper(), key=key))
            db.session.commit()

    @staticmethod
    def remove(name):
        try:
            ApiKeyModel.query.filter_by(name=name.upper()).remove()
            db.session.commit()
            return True
        except:
            return False
