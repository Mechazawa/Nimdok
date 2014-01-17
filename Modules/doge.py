#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2

from bs4 import BeautifulSoup

import events
import BotKit.util.irc as irc


command = ":doge"
def parse(bot, user, channel, msg):
    if msg.lower()[:len(command)+1].rstrip() == command:
        soup = BeautifulSoup(urllib2.urlopen("https://coinedup.com/OrderBook?market=DOGE&base=BTC").read())
        tag = [x for x in soup.findAll('li') if x.get('class') == ['active']][1]
        res = tag.text.strip().replace(")",'').split("(")
        bot.msg(channel, "%s %s" % (
            irc.Bold(res[0]),
            res[1]
        ))

events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)