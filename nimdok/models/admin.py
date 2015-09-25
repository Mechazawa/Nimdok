from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String


class AdminModel(declarative_base()):
    __tablename__ = 'admin'

    username = Column(String, unique=True, primary_key=True)

