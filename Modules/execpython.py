# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
from BotKit import command, stylize


#apiurl = "https://shell-27.appspot.com/"
apiurl = "http://py-ide-online.appspot.com/"
pykey  = ""
@command("py")
def parse(bot, channel, user, args):
    global pykey
    if pykey == "":
        pykey = pysession()
        if pykey == "":
            bot.msg(channel, "Could not obtain a session key")
            return
    url = "%sshell.do?&statement=%s&session=%s" % (apiurl, urllib2.quote(args), urllib2.quote(pykey))
    resp = urllib2.urlopen(url).read().rstrip()
    resp = resp.replace('\001', '')
    if '\n' in resp or '\r' in resp:
        paste = urllib2.urlopen("https://nnmm.nl/", urllib2.quote(resp)).read()
        bot.msg(channel, "%s: %s" % (user, paste))
    elif len(resp) > 300:
        bot.msg(channel, stylize.Trunicate(resp ,300))
        paste = urllib2.urlopen("https://nnmm.nl/", urllib2.quote(resp)).read()
        bot.msg(channel, "%s: %s" % (user, paste))
    else:
        bot.msg(channel, resp)

@command("newkey", True)
def newkey(bot, channel, user, args):
    global pykey
    pykey = pysession()
    bot.msg(channel, "Got a new key: %s" % pykey)

def pysession():
    resp = urllib2.urlopen(apiurl).read()
    soup = BeautifulSoup(resp)
    key = [x for x in soup.findAll('input') if x.has_attr('name') and x.get('name') == 'session'][0].get('value')
    return key
