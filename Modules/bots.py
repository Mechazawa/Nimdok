# -*- coding: utf-8 -*-
#!/usr/bin/python
from BotKit import *


@handles('msg')
def parse(bot, channel, user, msg):
    if msg.lower()[:6].rstrip() == ".bots":
        bot.msg(channel, 
                "Reporting in! " + 
                irc.SetColor("[Python] ", irc.Color.Blue) + 
                irc.SetColor("See " + irc.Bold("https://github.com/Mechazawa/Nimdok"), irc.Color.Cyan)
        )
