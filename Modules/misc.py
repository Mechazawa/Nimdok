#!/usr/bin/env python
# -*- coding: utf-8 -*-
from BotKit import command

@command("dongle")
def fork(bot, channel, user, arg):
  forkable = arg.split()[0] if len(arg.split()) else user
  bot.action(channel, "forks %s'%s dongle" % (forkable, "s" if forkable[-1].lower() not in "zxs" else ""))
