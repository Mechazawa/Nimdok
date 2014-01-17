# -*- coding: utf-8 -*-
#!/usr/bin/python
import urllib2
import json

import events
import BotKit.util.irc as irc


command = ":ltc"
def parse(bot, user, channel, msg):
    if msg.lower()[:len(command)+1].rstrip() == command:
        jo = json.loads(urllib2.urlopen("https://btc-e.com/api/2/ltc_usd/ticker").read())["ticker"]
        info = "%s %s$, %s %s$, %s %s$, %s %s$, %s %s" % (
            irc.Bold("Last:"), jo["last"],
            irc.Bold("High:"), jo["high"],
            irc.Bold("Low:"), jo["low"],
            irc.Bold("Avg:"), jo["avg"],
            irc.Bold("Vol:"), jo["vol"]
        )
        bot.msg(channel, info)


events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)