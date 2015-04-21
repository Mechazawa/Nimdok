# -*- coding: utf-8 -*-

import json
from urllib2 import urlopen, quote
from BotKit import command, stylize

USAGE = ':ud [-num] <word>'
UD_API = 'http://api.urbandictionary.com/v0/define?term={}'

@command("ud")
def parse(bot, channel, user, arg):
    pos = 0
    if arg.startswith('-'):
        try:
            opt, arg = arg.split(' ', 1)
            pos = int(opt.strip('-')) - 1  # Zero-based list access.
        except ValueError:
            bot.msg(channel, 'Bad argument -- usage, {}'.format(USAGE))
            return
    elif not arg:
        bot.msg(channel, 'Usage, {}'.format(USAGE))
        return

    url = UD_API.format(quote(arg))
    data = json.load(urlopen(url))

    if data['result_type'] == 'no_results':
        bot.msg(channel, '{}: That word is not defined.'.format(user))
        return

    L = data['list']
    pos = max(0, min(pos, len(L)-1))  # Ensure argument is within bounds.
    meaning = L[pos]['definition'].encode('utf-8')
    truncated = stylize.Truncate(meaning, 250)
    bot.msg(channel, '{}: {}'.format(user, truncated))
