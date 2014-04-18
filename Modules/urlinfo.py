# -*- coding: utf-8 -*-

import urllib2
import httplib2
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
                try: # urllib2
                    head = urllib2.urlopen(HeadRequest(m))
                except: # httplib2
                    h = httplib2.Http()
                    head = h.request(m, 'HEAD')
                else:
                    pass
            except:
                try:
                    source = urllib2.urlopen(m).read().replace('\r','').replace('\n','')
                except Exception, e:
                    bot.msg(channel, e)
                else:
                    bot.msg(channel, stylize.Trunicate(source))
            else:
                try: # urllib2
                    head.read()
                    mimetype = head.headers.type
                except: # httplib2
                    mimetype = head[0]['content-type']
                else:
                    pass
                if "html" in mimetype.lower():
                    try: # urllib2
                        source = urllib2.urlopen(m)
                        BS = BeautifulSoup(source)
                    except: # httplib2
                        h = httplib2.Http()
                        source = h.request(m)
                        BS = BeautifulSoup(source[1])
                    else:
                        pass
                    try:
                        title = BS.find('title').text.replace('\r', '').replace('\n', '').strip().encode('utf-8')
                    except:
                        pass
                        # no title tag found
                    else:
                        bot.msg(channel, title)
                    # bot.msg(channel, BS.find('title').text.replace('\r','').replace('\n','').strip().encode('utf-8'))
                elif "text" in mimetype.lower():
                    txt = urllib2.urlopen(m).read().replace("\n", " ").replace("\r", "")
                    bot.msg(channel, stylize.Trunicate(txt))
                else:
                    try: # urllib2
                        size = int(urllib2.urlopen(m).info().getheaders("Content-Length")[0])
                    except: # httplib2
                        size = int(head[0]['content-length'])
                    else:
                        pass
                    bot.msg(channel, 'Content-Type: ' + str(mimetype) + ' - ' + humanize.sizefmt(size))

def getdomain(s, nosub=False):
    domain = s.split('/')[2].split('?')[0]
    return domain.split('.', domain.count(".")-1)[-1] if nosub else domain
