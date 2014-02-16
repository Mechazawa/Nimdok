#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib2
from BotKit import command, stylize

@command("ud")
def parse(bot, channel, user, arg):
    apiurl = 'http://api.urbandictionary.com/v0/define?term=' + urllib2.quote(arg)
    data = json.load(urllib2.urlopen(apiurl))
    if len(arg) == 0:
        bot.msg(channel, 'Usage, :ud <word>')
    else:
        if 'no_results' in urllib2.urlopen(apiurl).read():
            bot.msg(channel, user + ': That word is not defined.')
        else:
            bot.msg(channel, user + ': ' + data['list'][0]['definition'])
