#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pydle import Client
from core import Module
from core.module import HookWrapper
from logging import Logger
from models import ModuleModel
import modules
import inspect


def _hook_glue(bot, methods):
    def hook_interface(*argv, **kwargs):
        for m in methods:
            m[1](m[0], bot, *argv, **kwargs)
    return hook_interface


class Nimdok(Client):
    instances = []
    hooked = []

    def __init__(self, *argv, **kwargs):
        super().__init__(*argv, **kwargs)
        self.init_modules()

    def init_modules(self):
        assert isinstance(self.logger, Logger)
        for hook in self.hooked:
            print("unhooking {}".format(hook))
            delattr(self, 'on_{}'.format(hook))

        self.hooked = []
        self.instances = []

        classes = self.list_modules()
        instances = []
        hooks = {}
        for c in classes:
            if not ModuleModel.is_enabled(c):
                print("Skipping {}".format(c.__name__))
                continue

            print("Initialising {}".format(c.__name__))
#            self.logger.info("Initialising {}".format(c.__name__))
            instances.append(c(self))
            module_hooks = [x[1] for x in inspect.getmembers(instances[-1]) if isinstance(x[1], HookWrapper)]

            for h in module_hooks:
                if h.hook_type not in hooks:
                    hooks[h.hook_type] = []

                hooks[h.hook_type].append((instances[-1], h))

        self.instances = instances
        for hook, methods in hooks.items():
            self.logger.debug('Registering hooks for on_{}'.format(hook))
            setattr(self, 'on_{}'.format(hook), _hook_glue(self, methods))
            self.hooked.append(hook)

    @staticmethod
    def list_modules():
        imported = [x[1] for x in inspect.getmembers(modules)
                    if "from 'nimdok/modules/" in str(x[1])]

        classes = []
        for i in map(inspect.getmembers, imported):
            file_classes = [
                x[1] for x in i
                if inspect.isclass(x[1]) and
                issubclass(x[1], Module) and
                x[1] is not Module
            ]

            for c in file_classes:
                classes.append(c)

        return classes

    @staticmethod
    def find_module(name):
        name = name.lower()
        for module in Nimdok.list_modules():
            if module.__name__.lower() == name:
                return module

        return None
