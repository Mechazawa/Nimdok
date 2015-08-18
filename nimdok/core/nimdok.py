#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pydle import Client
from core import Module
from core.module import HookWrapper
import modules
import inspect


def _hook_glue(hook_type, methods):
    def hook_interface(self, *argv, **kwargs):
        for m in methods:
            m(self, *argv, **kwargs)
    return hook_interface


class Nimdok(Client):
    def __init__(self, *argv, **kwargs):
        super().__init__(*argv, **kwargs)

        # There be dragons
        imported = [x[1] for x in inspect.getmembers(modules)
                    if "from 'nimdok/modules/" in str(x[1])]

        classes = []
        for i in map(inspect.getmembers, imported):
            list(map(classes.append, [
                x[1] for x in i
                if inspect.isclass(x[1])
                and issubclass(x[1], Module)
                and x[1] is not Module
            ]))

        instances = []
        hooks = {}
        for c in classes:
            print("Initialising {}".format(c.__name__))
            instances.append(c(self))
            module_hooks = [x[1] for x in inspect.getmembers(instances[-1]) if isinstance(x[1], HookWrapper)]

            for h in module_hooks:
                if h.hook_type not in hooks:
                    hooks[h.hook_type] = []

                hooks[h.hook_type].append(h)

        for hook, methods in hooks.items():
            setattr(self, 'on_{}'.format(hook), _hook_glue(hook, methods))


