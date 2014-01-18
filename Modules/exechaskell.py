#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json
from BotKit import command, stylize


apiurl = "http://tryhaskell.org/haskell.json?method=eval&expr="
@command("hs")
def parse(bot, channel, user, args):
    resp = json.loads(urllib2.urlopen(apiurl + urllib2.quote(args)).read())
    message = ""
    if 'error' in resp:
        message += resp['error']+"\n\n"
    if 'result' in resp:
        message += ' => '+resp['result']+"\n\n"
    #if ke(resp, 'type'):
    #    message += ' :: '+resp['type']+"\n\n"
    if 'exception' in resp:
        message += ' !! '+resp['exception']+"\n\n"
    message = message.strip()
    print message
    if '\n' in message or '\r' in message:
        print urllib2.quote(args+"\n\n"+message)
        paste = urllib2.urlopen("http://nnmm.nl/", urllib2.quote(args+"\n\n"+message)).read()
        bot.msg(channel, "%s: %s" % (user, paste))
    elif len(message) > 300:
        bot.msg(channel, stylize.Trunicate(message ,300))
        paste = urllib2.urlopen("http://nnmm.nl/", urllib2.quote(args+"\n\n"+message)).read()
        bot.msg(channel, "%s: %s" % (user, paste))
    else:
        bot.msg(channel, message)
