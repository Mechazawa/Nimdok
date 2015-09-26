from sqlalchemy.ext.declarative import declarative_base as sqa_declarative_base

engine = None
db_session = None

declarative_base = sqa_declarative_base()

