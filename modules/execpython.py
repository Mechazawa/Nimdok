#!/usr/bin/env python
# -*- coding: utf-8 -*-

import events
import urllib2
from bs4 import BeautifulSoup
import Util.irc as ircutil

#apiurl = "https://shell-27.appspot.com/"
apiurl = "http://py-ide-online.appspot.com/"
pykey  = "" 
command = ":py"
def parse(bot, user, channel, msg):
    if msg.lower()[:len(":newkey")+1].rstrip() == ":newkey":
        pykey = pysession()    
        bot.msg(channel, "Got a new key: %s" % pykey)
    if msg.lower()[:len(command)+1].rstrip() == command:
        global pykey
        if pykey == "":
            pykey = pysession()
            if pykey == "": 
                bot.msg(channel, "Could not obtain a session key")
                return

        args = msg[len(command)+1:]
        url = "%sshell.do?&statement=%s&session=%s" % (apiurl, urllib2.quote(args), urllib2.quote(pykey))
        resp = urllib2.urlopen(url).read().rstrip()
        if '\n' in resp or '\r' in resp:
            paste = urllib2.urlopen("http://nnmm.nl/", urllib2.quote(resp)).read()
            bot.msg(channel, "%s: %s" % (user, paste))
        elif len(resp) > 300:
            bot.msg(channel, ircutil.Trunicate(resp ,300))
            paste = urllib2.urlopen("http://nnmm.nl/", urllib2.quote(resp)).read()
            bot.msg(channel, "%s: %s" % (user, paste))
        else:
            bot.msg(channel, resp)


def pysession():
    resp = urllib2.urlopen(apiurl).read()
    soup = BeautifulSoup(resp)
    key = [x for x in soup.findAll('input') if x.has_attr('name') and x.get('name') == 'session'][0].get('value')
    return key


events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)