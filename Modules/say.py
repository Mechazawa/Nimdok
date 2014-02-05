# -*- coding: utf-8 -*-
#!/usr/bin/python
from BotKit import *

@command('say')
def parse(bot, channel, user, msg):
    bot.msg(channel, msg)
