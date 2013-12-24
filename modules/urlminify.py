#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import events
import Util.net as netutil

ignoreddomains = ["youtube.com", "youtu.be", "4chan.org", "twitter.com"]
command = ":minify"
def parse(bot, user, channel, msg):
    global lasturl
    if msg.lower()[:len(command)+1].rstrip() == command:
    	if lasturl:
        	bot.msg(channel, "%s: %s" % (user, urllib2.urlopen("http://tinyurl.com/api-create.php?url="+urllib2.quote(lasturl)).read()))
        else:
        	bot.msg(channel, "Nothing to minify")
    else:
        for m in msg.split(' '):
            if m[:4] == "http" and '//' in m[5:-len(m)+8]:
                lasturl = m


lasturl = ""
events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)