from sqlalchemy import Column, String
from .shared import declarative_base


class AdminModel(declarative_base):
    __tablename__ = 'admin'

    def __init__(self, username):
        self.username = username

    username = Column(String, unique=True, primary_key=True)

