from sqlalchemy import Column, String
from .shared import declarative_base, db


class IgnoredDomainModel(declarative_base):
    __tablename__ = 'ignored_domains'

    def __init__(self, domain):
        self.domain = domain

    domain = Column(String, unique=True, primary_key=True)

    @staticmethod
    def is_ignored(domain):
        return IgnoredDomainModel.query \
                   .filter_by(domain=domain.upper()) \
                   .count() > 0

    @staticmethod
    def add(domain):
        try:
            db.session.add(IgnoredDomainModel(domain.upper()))
            db.session.commit()
            return True
        except:
            return False

    @staticmethod
    def remove(domain):
        try:
            IgnoredDomainModel.query.filter_by(domain=domain.upper()).remove()
            db.session.commit()
            return True
        except:
            return False
