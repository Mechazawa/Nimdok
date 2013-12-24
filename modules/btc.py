#!/usr/bin/env python
# -*- coding: utf-8 -*-

import events
import urllib2
import json
import Util.irc as irc

command = ":btc"
def parse(bot, user, channel, msg):
    if msg.lower()[:len(command)+1].rstrip() == command:
        jo = json.loads(urllib2.urlopen("https://mtgox.com/api/1/BTCUSD/public/ticker").read())["return"]
        info = "%s %s, %s %s, %s %s, %s %s , %s %s" % (
            irc.Bold("Last:"), jo["last"]["display"],
            irc.Bold("High:"), jo["high"]["display"],
            irc.Bold("Low:"), jo["low"]["display"],
            irc.Bold("Avg:"), jo["avg"]["display"],
            irc.Bold("Vol:"), jo["vol"]["display"]
        )
        bot.msg(channel, info.encode('utf-8', 'ignore'))

events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)