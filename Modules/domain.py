# -*- coding: utf-8 -*-
from BotKit import command, stylize
from urllib2 import urlopen
import json

url = "https://instantdomainsearch.com/all/%s?tlds=%s&limit=20"

@command("domain")
def check_domain(bot, channel, user, arg):
    args = arg.split()
    if len(args) < 2:
        bot.msg(channel, "Usage: :domain example com net org")
    else:
        domain = args[0]
        del args[0]

        resp = dict(zip(*[tuple(args), (False for _ in range(len(args)))]))
        raw = urlopen(url % (domain, ','.join(args))).read()
        for r in raw.strip().split('\n'):
            js = json.loads(r)
            if 'isRegistered' in js:
                resp[js['tld']] = js['isRegistered']

        out = domain
        taken = ""
        avail = ""
        for dmn in resp:
            if resp[dmn]:
                taken += " " + dmn
            else:
                avail += " " + dmn

        if avail:
            out += " A:" + avail
        if taken:
            out += " T:" + taken
        bot.msg(channel, out)
