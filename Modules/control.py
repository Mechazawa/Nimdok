# -*- coding: utf-8 -*-
from BotKit import command

@command('part', True)
def parse(bot, channel, user, msg):
    bot.part(msg.split()[0])
