# -*- coding: utf-8 -*-
#!/usr/bin/python
import events
import urllib2
from bs4 import BeautifulSoup

command = ":isup"
def parse(bot, user, channel, msg):
    if msg.lower()[:len(command)+1].rstrip() == command:
        msg = msg[len(command)+1:].strip()
        if len(msg) == 0:
            bot.msg(channel, "%s: Usage, :isup [url]" % user)
        else:
            soup = BeautifulSoup(urllib2.urlopen("http://www.isup.me/" + urllib2.quote(msg)).read())
            response = soup.body.text.strip().split('\n')[0]
            bot.msg(channel, "%s: %s" % (user, response))

events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)
