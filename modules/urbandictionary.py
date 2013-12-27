#!/usr/bin/env python
# -*- coding: utf-8 -*-

import events
import urllib2
from bs4 import BeautifulSoup
import Util.irc as ircutil

command = ":ud"
def parse(bot, user, channel, msg):
    if msg.lower()[:len(command)+1].rstrip() == command:
        msg  = msg[len(command)+1:]
        resp = urllib2.urlopen("http://www.urbandictionary.com/define.php?term=" + urllib2.quote(msg)).read()
        if "isn't defined." in resp:
            bot.msg(channel, "%s: That word is not defined" % user)
        else:
            soup = BeautifulSoup(resp)
            meaning = [x for x in [i for i in soup.findAll("div") if i.get("id") and "entry_" in i.get("id")][0].findAll("div") if x.get('class') and x.get('class') == ['definition']][0].text.replace("\n", " ")
            if len(meaning) > 300:
                bot.msg(channel, ircutil.Trunicate(meaning ,300))
                ircutil.SetMore(meaning)
            else:
                bot.msg(channel, meaning)


events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)