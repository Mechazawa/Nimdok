#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from BotKit import command


@command("more")
def parse(bot, user, channel, arg):
    more = bot.GetMore()
    if more.strip():
        bot.msg(channel, "%s: %s" % (user, urllib2.urlopen("http://nnmm.nl/", more).read()))
    else:
        bot.msg(channel, "There is nothing more :/")