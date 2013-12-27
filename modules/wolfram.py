#!/usr/bin/env python
# -*- coding: utf-8 -*-

import events
import urllib2
import Util.irc as ircutil
import lxml.etree as et


apiurl="http://api.wolframalpha.com/v2/query?"
#set params
apiurl+="units=metric&location=Amsterdam&reinterpret=true&format=plaintext&excludepodid=Input&"
wolframkey=""
command=":wa"
def parse(bot, user, channel, msg):
  if msg.lower()[:len(command)+1].rstrip() == command:
    msg = msg[len(command)+1:]
    
    #build url
    url = apiurl + "appid=" + wolframkey
    url += "&input=" + urllib2.quote(msg)
    
    #get result
    raw = urllib2.urlopen(url).read()
    tree = et.fromstring(raw)

    #parse result
    if tree.get('error') != 'false':
      bot.msg(channel, "Wolfram alpha returned an error")
    elif tree.get('numpods') > 0:
      result = tree.find('pod').find('subpod').find('plaintext').text
      bot.msg(channel, "%s: %s" % (user, ircutil.Trunicate(result.split('\n')[0] ,300)))
      if len(result) > 300 or '\n' in result:
          ircutil.SetMore(result)
    elif len(tree.findall('tips')) > 0:
        bot.msg(channel, "%s: %s" % (user, tree.find('tips').find('tip').get('text')))
    else:
        bot.msg(channel, "%s: I didn't find what you were looking for" % user)

events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)


#obtain the wolfram alpha key
with open("../../wolframkey", 'r') as f:
    wolframkey = f.read()