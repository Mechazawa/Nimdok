# -*- coding: utf-8 -*-
#!/usr/bin/python
from BotKit import *

@command('msg', True)
def parse(bot, channel, user, msg):
    bot.msg(msg.split()[0], msg.replace(msg.split()[0], '').strip())

@command('join', True)
def parse(bot, channel, user, msg):
    bot.join(msg.split()[0])

@command('part', True)
def parse(bot, channel, user, msg):
    bot.part(msg.split()[0])

@command('notice', True)
def parse(bot, channel, user, msg):
    bot.notice(msg.split()[0], msg.replace(msg.split()[0], '').strip())
