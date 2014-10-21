# -*- coding: utf-8 -*-
from BotKit import command, stylize
import pythonwhois as who


def taken(dmn):
    info = who.get_whois(dmn)
    if "status" in info:
        return "clientDeleteProhibited" in info['status']
    if 'registrar' in info:
        return True
    if "contacts" in info:
        return False in [info['contacts'].get(x, None) is None for x in ['admin', 'tech', 'registrant', 'billing']]
    return False


@command("domain")
def check_domain(bot, channel, user, arg):
    args = arg.split()
    if len(args) < 2:
        bot.msg(channel, "Usage: :domain example com net org")
    else:
        domain = args[0]
        del args[0]

        out = domain
        for tld in args:
            out += " " + stylize.Invert(stylize.SetColor(
                tld, stylize.Color.Red if taken("%s.%s" % (domain, tld)) else stylize.Color.Green
            ))
        bot.msg(channel, out)
