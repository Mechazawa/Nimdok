# -*- coding: utf-8 -*-
#!/usr/bin/python
from BotKit import command
import urllib2

@command("lmgtfy")
def parse(bot, channel, user, arg):
    if len(arg) == 0:
        bot.msg(channel, "Usage: :lmgtfy [text]")
    else:
        bot.msg(channel, user+": http://lmgtfy.com/?q="+urllib2.quote(arg))

@command("lmddgtfy")
def parse(bot, channel, user, arg):
    if len(arg) == 0:
        bot.msg(channel, "Usage: :lmddgtfy [text]")
    else:
        bot.msg(channel, user+": http://lmddgtfy.net/?q="+urllib2.quote(arg))

