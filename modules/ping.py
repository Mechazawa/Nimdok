# -*- coding: utf-8 -*-
#!/usr/bin/python
import events

command = ":ping"
def parse(bot, user, channel, msg):
    if msg.lower()[:len(command)+1].rstrip() == command:
        bot.msg(channel, user+": PONG")


events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)