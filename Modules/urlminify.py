#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from BotKit import command, handles

@command("minify")
def parse(bot, channel, user, arg):
    global lasturl
    if lasturl:
        bot.msg(channel, "%s: %s" % (user, urllib2.urlopen("http://nnmm.nl/", lasturl).read()))
    else:
        bot.msg(channel, "Nothing to minify")

@handles('msg')
def monitor(bot, channel, user, msg):
    global lasturl
    for m in msg.split(' '):
        if m[:4] == "http" and '//' in m[5:-len(m)+8]:
            lasturl = m
