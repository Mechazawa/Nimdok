#!/usr/bin/env python
# -*- coding: utf-8 -*-

import events


command = ":help"
def parse(bot, user, channel, msg):
    if msg.lower()[:len(command)+1].rstrip() == command:
        bot.msg(channel, "For how to use me go to http://nnmm.nl/dumbot or read the code http://nnmm.nl/viewcode.php")

events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)