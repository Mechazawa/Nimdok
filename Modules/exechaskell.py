#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json

import events
import BotKit.util.irc as ircutil


command = ":hs"
apiurl = "http://tryhaskell.org/haskell.json?method=eval&expr="
def parse(bot, user, channel, msg):
    if msg.lower()[:len(command)+1].rstrip() == command:
        args = msg[len(command)+1:]
        print args
        resp = json.loads(urllib2.urlopen(apiurl + urllib2.quote(args)).read())
        print resp
        message = ""
        if ke(resp, 'error'):
            message += resp['error']+"\n\n"
        if ke(resp, 'result'):
            message += ' => '+resp['result']+"\n\n"
        #if ke(resp, 'type'):
        #    message += ' :: '+resp['type']+"\n\n"
        if ke(resp, 'exception'):
            message += ' !! '+resp['exception']+"\n\n"
        message = message.strip()
        print message
        if '\n' in message or '\r' in message:
            print urllib2.quote(args+"\n\n"+message)
            paste = urllib2.urlopen("http://nnmm.nl/", urllib2.quote(args+"\n\n"+message)).read()
            bot.msg(channel, "%s: %s" % (user, paste))
        elif len(message) > 300:
            bot.msg(channel, ircutil.Trunicate(message ,300))
            paste = urllib2.urlopen("http://nnmm.nl/", urllib2.quote(args+"\n\n"+message)).read()
            bot.msg(channel, "%s: %s" % (user, paste))
        else:
            bot.msg(channel, message)

def ke(a, k):
    try: 
        a[k]
        return True
    except: 
        return False


events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)