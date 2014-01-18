# -*- coding: utf-8 -*-
#!/usr/bin/python

from BotKit import handles
import datetime

@handles('msg')
def parse(bot, channel, user, msg):
    with open('chat.log', 'a') as log:
        log.write("[%s] %s %s: %s\n" % (datetime.datetime.now().strftime("%m-%d %H:%M:%S"), channel, user, msg))
