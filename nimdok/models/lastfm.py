from sqlalchemy import Column, String
from .shared import declarative_base


class LastfmModel(declarative_base):
    __tablename__ = 'lastfm'

    def __init__(self, irc_name, lastfm_name):
        self.irc_name = irc_name
        self.lastfm_name = lastfm_name

    irc_name = Column(String, unique=True, primary_key=True)
    lastfm_name = Column(String)

    @staticmethod
    def set(irc_name, lastfm_name):
        irc_name = irc_name.upper().strip()
        LastfmModel.delete(irc_name)
        db.session.add(LastfmModel(irc_name, lastfm_name))
        db.session.commit()
        return True

    @staticmethod
    def delete(irc_name):
        irc_name = irc_name.upper().strip()
        LastfmModel.query.filter_by(irc_name=irc_name).remove()
        db.session.commit()
        return True

    @staticmethod
    def get(irc_name):
        irc_name = irc_name.upper().strip()
        return LastfmModel.query \
            .filter_by(name=irc_name) \
            .first()
