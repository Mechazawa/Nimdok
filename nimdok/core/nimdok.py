#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pydle import Client
import inspect


class Nimdok(Client):
    def on_connect(self):
        self.join('#/g/spam')

        print("building list of modules")

