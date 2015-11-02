from sqlalchemy.ext.declarative import declarative_base as sql_declarative_base


class db(object):
    engine = None
    session = None

declarative_base = sql_declarative_base()

