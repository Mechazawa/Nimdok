# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
from BotKit import command, stylize


@command("doge")
def parse(bot, channel, user, args):
    soup = BeautifulSoup(urllib2.urlopen("https://coinedup.com/OrderBook?market=DOGE&base=BTC").read())
    tag = [x for x in soup.findAll('li') if x.get('class') == ['active']][1]
    res = tag.text.strip().replace(")",'').split("(")
    bot.msg(channel, "%s %s" % (
        stylize.Bold(res[0]),
        res[1]
    ))