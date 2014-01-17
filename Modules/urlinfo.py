#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
from BotKit import util as netutil
import events
import BotKit.util.irc as ircutil
import BotKit.util.human as humanutil


class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"


ignoreddomains = ["youtube.com", "youtu.be", "4chan.org", "twitter.com"]
def parse(bot, user, channel, msg):
    for m in msg.split(' '):
        if m[:4] == "http" and '//' in m[5:-len(m)+8]:
            if netutil.getdomain(m, True) in ignoreddomains: continue
            try:
                head = urllib2.urlopen(HeadRequest(m))
                head.read()
                mimetype = head.headers.type
                if "html" in mimetype.lower():
                    dta = urllib2.urlopen(m).read()
                    ret = dta if '<title>' not in dta.lower() else BeautifulSoup(dta).title.text.strip()
                    bot.msg(channel, ircutil.Trunicate(ret, 150).replace("\r", "").replace("\n", ""))
                elif "text" in mimetype.lower():
                    txt = urllib2.urlopen(m).read()
                    bot.msg(channel, ircutil.Trunicate(txt.replace("\n", " ").replace("\r", "")))
                else:
                    size = int(urllib2.urlopen(m).info().getheaders("Content-Length")[0])
                    bot.msg(channel, "%s | %s" % (mimetype, humanutil.sizefmt(size)))
            except Exception, e: print e

events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)