#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BotKit import command


@command("help")
def parse(bot, channel, user, msg):
    bot.msg(channel, "For how to use me go to http://nnmm.nl/dumbot or read the code http://nnmm.nl/viewcode.php")
