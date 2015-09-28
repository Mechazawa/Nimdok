from sqlalchemy.ext.declarative import declarative_base as sqa_declarative_base


class db(object):
    engine = None
    session = None

declarative_base = sqa_declarative_base()

