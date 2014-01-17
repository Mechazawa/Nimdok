#!/usr/bin/env python
# -*- coding: utf-8 -*-

import events

cmd=":dongle"
def parse(bot, user, channel, msg):
    if msg[:len(cmd)+1].rstrip() == cmd:
        bot.action(channel, "forks %s's dongle" % user)

events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)