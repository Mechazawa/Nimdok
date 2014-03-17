#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json

from BotKit import command, stylize


@command("btc")
def parse(bot, channel, user, args):
    data = json.load(urllib2.urlopen('https://www.bitstamp.net/api/ticker/'))
    text = u'BTC · Last: ' + data['last'] + u'$ · High: ' + data['high'] + u'$ · Low: ' \
            + data['low'] + u'$ · Volume: ' + data['volume'] + u' · BitStamp'
    bot.msg(channel, text.encode('utf-8'))
