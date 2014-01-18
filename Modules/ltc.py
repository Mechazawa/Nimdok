# -*- coding: utf-8 -*-
#!/usr/bin/python
import urllib2
import json
from BotKit import command, stylize

@command("ltc")
def parse(bot, channel, user, msg):
    jo = json.loads(urllib2.urlopen("https://btc-e.com/api/2/ltc_usd/ticker").read())["ticker"]
    info = "%s %s$, %s %s$, %s %s$, %s %s$, %s %s" % (
        stylize.Bold("Last:"), jo["last"],
        stylize.Bold("High:"), jo["high"],
        stylize.Bold("Low:"), jo["low"],
        stylize.Bold("Avg:"), jo["avg"],
        stylize.Bold("Vol:"), jo["vol"]
    )
    bot.msg(channel, info)
