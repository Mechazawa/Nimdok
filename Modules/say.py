# -*- coding: utf-8 -*-
from BotKit import *

@command('say')
def parse(bot, channel, user, msg):
    bot.msg(channel, msg)
