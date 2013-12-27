#!/usr/bin/env python
# -*- coding: utf-8 -*-

import events
import urllib2
from bs4 import BeautifulSoup
import Util.irc as ircutil

command = ":more"
def parse(bot, user, channel, msg):
    if msg.lower()[:len(command)+1].rstrip() == command:
    	more = ircutil.GetMore()
    	if more.strip():
        	bot.msg(channel, "%s: %s" % (user, urllib2.urlopen("http://nnmm.nl/", more).read()))
        else:
        	bot.msg(channel, "There is nothing more :/")


events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)