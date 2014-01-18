# -*- coding: utf-8 -*-
#!/usr/bin/python
from BotKit import *
import BotKit.util.stylize as irc

command = ".bots"

@handles('msg')
def parse(bot, user, channel, msg):
    if msg.lower()[:len(command)+1].rstrip() == command:
        bot.msg(channel, 
                "Reporting in! " + 
                irc.SetColor("[Python] ", irc.Color.Blue) + 
                irc.SetColor("See " + irc.Bold("http://nnmm.nl/dumbot"), irc.Color.Cyan)
        )
