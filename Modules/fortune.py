#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BotKit import command
import os

@command("fortune")
def parse(bot, user, channel, msg):
    bot.msg(channel, ' '.join(os.popen("fortune -a fortunes").readlines()).strip())
