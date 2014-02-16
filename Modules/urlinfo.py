#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
from BotKit import handles, humanize, stylize

class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"

ignoreddomains = ["youtube.com", "youtu.be", "4chan.org", "twitter.com"]
@handles('msg')
def parse(bot, channel, user, msg):
    for m in msg.split(' '):
        if m[:4] == "http" and '//' in m[5:-len(m)+8]:
            if getdomain(m, True) in ignoreddomains:
                continue
            try: 
                head = urllib2.urlopen(HeadRequest(m))
            except: 
                try:
                    source = urllib2.urlopen(m).read().replace('\r','').replace('\n','')
                except Exception, e:
                    bot.msg(channel, e)
                else:
                    bot.msg(channel, stylize.Trunicate(source))
            else:
                head.read()
                mimetype = head.headers.type
                if "html" in mimetype.lower():
                    source = urllib2.urlopen(m)
                    BS = BeautifulSoup(source)
                    bot.msg(channel, BS.find('title').text.replace('\r','').replace('\n','').strip().encode('utf-8'))
                elif "text" in mimetype.lower():
                    txt = urllib2.urlopen(m).read().replace("\n", " ").replace("\r", "")
                    bot.msg(channel, stylize.Trunicate(txt))
                else:
                    size = int(urllib2.urlopen(m).info().getheaders("Content-Length")[0])
                    bot.msg(channel, 'Content-Type: ' + str(mimetype) + ' - ' + humanize.sizefmt(size))

def getdomain(s, nosub=False):
    domain = s.split('/')[2].split('?')[0]
    return domain.split('.', domain.count(".")-1)[-1] if nosub else domain
