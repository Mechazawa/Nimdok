# -*- coding: utf-8 -*-
#!/usr/bin/python
from BotKit import command

@command("ping")
def parse(bot, user, channel, arg):
    bot.msg(channel, user+": PONG motherfucker!")
