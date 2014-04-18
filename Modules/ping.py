# -*- coding: utf-8 -*-
from BotKit import command

@command("ping")
def parse(bot, channel, user, arg):
    bot.msg(channel, user+": PONG motherfucker!")
