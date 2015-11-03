from sqlalchemy import Column, String
from .shared import declarative_base, db
from inspect import isclass
from core import Module


class ModuleModel(declarative_base):
    __tablename__ = 'mods_enabled'

    def __init__(self, name):
        self.name = name

    name = Column(String, unique=True, primary_key=True)

    @staticmethod
    def _get_module_name(obj):
        if isclass(obj) and issubclass(obj, Module):
            return obj.__name__.upper()
        elif not isinstance(obj, str):
            raise ValueError("Expected subclass of 'Module' got {}".format(type.__str__(obj)))

        return obj.upper()

    @staticmethod
    def enable(obj):
        obj = ModuleModel._get_module_name(obj)
        if ModuleModel.is_enabled(obj):
            return False

        db.session.add(ModuleModel(obj))
        db.session.commit()
        return True

    @staticmethod
    def is_enabled(obj):
        obj = ModuleModel._get_module_name(obj)
        return ModuleModel.query.filter_by(name=obj).count() > 0

    @staticmethod
    def list_enabled():
        return list(map(lambda x: x.name,
                        ModuleModel.query.all()))

    @staticmethod
    def disable(obj):
        obj = ModuleModel._get_module_name(obj)
        if not ModuleModel.is_enabled(obj):
            return False

        ModuleModel.query.filter_by(name=obj).remove()
        db.session.commit()
        return True
