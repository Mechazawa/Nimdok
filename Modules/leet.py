# -*- coding: utf-8 -*-
from BotKit import command
from random import randrange as rand

replacements = {
  "to":"2", "too":"2",
  "for":"4", "you": "u",
  "a": "4", "e": "3",
  "i": "1", "l": "1",
  "z": "2", "s": "5",
  "t": "7", "b": "8",
  "g": "9", "o": "0",
  " ": "_", "'": "*"
}

@command("leet")
def parse(bot, channel, user, arg):
    if len(arg) == 0:
        bot.msg(channel, "Usage: :leet [text]")
    else:
        msg = arg.lower()
        #make it l337
        for r in replacements:
            msg = msg.replace(r, replacements[r])
        #random capitals!
        msg = ''.join([c.upper() if rand(3) == 1 else c for c in msg])
        bot.msg(channel, msg)
