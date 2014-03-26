#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BotKit import *
import Modules
import apikeys
try:
    from setproctitle import setproctitle
    setproctitle("Nimdok")
except ImportError:
    pass

irc = BotKit(
    host= "irc.rizon.net",
    port= 9999,
    ssl= True,

    nickname= "Nimdok",
    nickpass=apikeys.botpass,

    channels= ["#/g/SICP", "#/g/Spam", "#/g/bots", "#/g/Summer", "#butthole", "#cockmail"],
    debug= True,
#    verbose=True
)

#general bot stuff
@handles('invite')
def invite(bot, channel, user):
    bot.logger.info("Invited to #%s" % channel)
    bot.join(channel)

@handles('msg')
def msg(bot, channel, user, msg):
    bot.logger.info("%s %s: %s" % (channel, user, msg))
    
@command('die', True)
def die(bot, channel, user, msg):
    bot.msg(channel, "o-okay then")
    bot.quit("Suicide")

irc.run()
