# -*- coding: utf-8 -*-
#!/usr/bin/python
from BotKit import handles


@handles("ctcp_version")
def version(bot, channel, user, msg):
    bot.logger.info("%s requested version info" % user)
    bot.notice(user, "\001VERSION You are now breathing manually\001")


@handles("ctcp_finger")
def finger(bot, channel, user, msg):
    bot.logger.info("%s tried to finger me")
    bot.notice(user, "\001FINGER have we met?\001")