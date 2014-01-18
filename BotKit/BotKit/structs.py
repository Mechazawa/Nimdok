#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Struct-ish stuff

class Message(object):
    def __init__(self, line):
        line = line.split(' :', 1)
        split = line[0].split(' ', 2)
        self.prefix = split[0]
        self.command = split[1]
        self.arguments = split[2] if len(split) >= 3 else False
        self.trailing = line[1] if len(line) == 2 else False

