#!/usr/bin/env python
# -*- coding: utf-8 -*-

import callback as call
import connection as con

class connection(con.connection):
    pass

class callback(call.callback):
    pass

class commands(object):
    def _parseArgs(self, args, parseInt=True):
        c = compile(r"""("[^"]*")|([^\s]+)""").findall(args)
        if parseInt:
            return [int(row[1]) if row[1].replace('-','').isdigit() else row[1] for row in c]
        else:
            return c
