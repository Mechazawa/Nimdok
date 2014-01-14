# -*- coding: utf-8 -*-
#!/usr/bin/python
import events
import Util.irc as irc

command = ".bots"
def parse(bot, user, channel, msg):
    if msg.lower()[:len(command)+1].rstrip() == command:
        bot.msg(channel, 
                "Reporting in! " + 
                irc.SetColor("[Python] ", irc.Color.Blue) + 
                irc.SetColor("See " + irc.Bold("http://nnmm.nl/dumbot"), irc.Color.Cyan)
        )


events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)
