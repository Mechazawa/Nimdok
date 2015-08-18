#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pydle import Client
from core import Module
import modules
import inspect


class Nimdok(Client):
    def __init__(self, *argv, **kwargs):
        super().__init__(*argv, **kwargs)

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

        print(classes)
