# -*- coding: utf-8 -*-

from BotKit import command
import os

@command("fortune")
def parse(bot, channel, user, msg):
    bot.msg(channel, ' '.join(os.popen("fortune -a fortunes").readlines()).strip())
