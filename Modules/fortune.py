#!/usr/bin/env python
# -*- coding: utf-8 -*-

import events
import os

command = ":fortune"
def parse(bot, user, channel, msg):
    if msg.lower()[:len(command)+1].rstrip() == command:
        bot.msg(channel, ' '.join(os.popen("fortune -a fortunes").readlines()).strip())

events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)