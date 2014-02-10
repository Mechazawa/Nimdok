#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from BotKit import command


@command("more")
def parse(bot, channel, user, arg):
    more = bot.GetMore().strip().replace("\r", "")
    if more:
        if more.count("\n") > 3 or len(more) > 1000:
            bot.msg(channel, "%s: %s" % (user, urllib2.urlopen("http://nnmm.nl/", more).read()))
        else:
            bot.msg(channel, more)
    else:
        bot.msg(channel, "There is nothing more :/")
