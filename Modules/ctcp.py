# -*- coding: utf-8 -*-
#!/usr/bin/python
from BotKit import handles

@handles("ctcp_version")
def version(bot, channel, user, msg):
    bot.logger.info("%s requested version info" % user)
    bot.msg(user, "\001VERSION You are now breathing manually\001")