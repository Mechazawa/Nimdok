#!/usr/bin/env python
# -*- coding: utf-8 -*-

import events
import Util.irc as ircutil

command = ":undress"
def parse(bot, user, channel, msg):
    if msg.lower()[:len(command)+1].rstrip() == command:
        bot.msg(channel, "Current code: http://nnmm.nl/viewcode.php " + ircutil.SetColor("HEAVY WIP!", ircutil.Color.Red))

events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)