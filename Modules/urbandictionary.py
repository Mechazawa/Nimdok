#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2

from bs4 import BeautifulSoup

import events
import BotKit.util.irc as ircutil


command = ":ud"
def parse(bot, user, channel, msg):
    if msg.lower()[:len(command)+1].rstrip() == command:
        msg  = msg[len(command)+1:]
        resp = urllib2.urlopen("http://www.urbandictionary.com/define.php?term=" + urllib2.quote(msg)).read()
        if "isn't defined." in resp:
            bot.msg(channel, "%s: That word is not defined" % user)
        else:
            soup = BeautifulSoup(resp)
            definitions = [x for x in soup.findAll("div") if x.get('class') and x.get('class') == ['definition']]
            examples = [x for x in soup.findAll("div") if x.get('class') and x.get('class') == ['example']]
            meaning = definitions[0].text.replace('\r', '').strip()
            if len(meaning) > 300:
                bot.msg(channel, ircutil.Trunicate(meaning.replace("\n", " ") ,300))
            else:
                bot.msg(channel, meaning.replace("\n", " "))
            ircutil.SetMore("%s\n\nExample:\n%s" % (meaning, examples[0].text.strip()))


events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)