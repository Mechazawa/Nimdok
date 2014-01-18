#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BotKit import command, stylize

@command("undress")
def undress(bot, channel, user, msg):
    bot.msg(channel, "Current code: https://github.com/Mechazawa/Nimdok " + stylize.SetColor("HEAVY WIP!", stylize.Color.Red))
