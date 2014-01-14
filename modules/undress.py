#!/usr/bin/env python
# -*- coding: utf-8 -*-

import events
import Util.irc as ircutil

sources = {
        ":undress" : "Current code: http://nnmm.nl/viewcode.php " + ircutil.SetColor("HEAVY WIP!", ircutil.Color.Red),
        ":git"     : "Git repo: https://github.com/Mechazawa/Nimdok (may be older then the current bot tho)"
}
def parse(bot, user, channel, msg):
  for x in sources:
    if msg.lower()[:len(x)+1].rstrip() == x:
        bot.msg(channel, sources[x])

events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)
