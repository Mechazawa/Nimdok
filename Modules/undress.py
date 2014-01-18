#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BotKit import command, stylize

@command("undress")
def undress(bot, user, channel, msg):
    bot.msg(channel, "Current code: http://nnmm.nl/viewcode.php " + stylize.SetColor("HEAVY WIP!", stylize.Color.Red))

@command("git")
def git(bot, use, channel, msg):
    bot.msg(channel,"Git repo: https://github.com/Mechazawa/Nimdok (may be older then the current bot tho)")