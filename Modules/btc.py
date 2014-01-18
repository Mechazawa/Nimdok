#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json

from BotKit import command, stylize


@command("btc")
def parse(bot,  channel, user, args):
    jo = json.loads(urllib2.urlopen("https://mtgox.com/api/1/BTCUSD/public/ticker").read())["return"]
    info = "%s %s, %s %s, %s %s, %s %s , %s %s" % (
        stylize.Bold("Last:"), jo["last"]["display"],
        stylize.Bold("High:"), jo["high"]["display"],
        stylize.Bold("Low:"), jo["low"]["display"],
        stylize.Bold("Avg:"), jo["avg"]["display"],
        stylize.Bold("Vol:"), jo["vol"]["display"]
    )
    bot.msg(channel, info.encode('utf-8', 'ignore'))
