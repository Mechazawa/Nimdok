#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pydle import Client
from core import Module
from core.module import HookWrapper
from logging import Logger
import modules
import inspect


def _hook_glue(bot, methods):
    def hook_interface(*argv, **kwargs):
        for m in methods:
            m[1](m[0], bot, *argv, **kwargs)
    return hook_interface


class Nimdok(Client):
    instances = []

    def __init__(self, *argv, **kwargs):
        super().__init__(*argv, **kwargs)
        self.init_modules()

    def init_modules(self):
        assert isinstance(self.logger, Logger)
        # There be dragons
        imported = [x[1] for x in inspect.getmembers(modules)
                    if "from 'nimdok/modules/" in str(x[1])]

        classes = []
        for i in map(inspect.getmembers, imported):
            list(map(classes.append, [
                x[1] for x in i
                if inspect.isclass(x[1]) and
                issubclass(x[1], Module) and
                x[1] is not Module
            ]))

        instances = []
        hooks = {}
        for c in classes:
            self.logger.info("Initialising {}".format(c.__name__))
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
