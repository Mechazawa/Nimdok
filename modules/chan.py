# -*- coding: utf-8 -*-
#!/usr/bin/python

import urllib2
import json
import events
import re
import Util.irc as irc
import Util.net as netutil
from bs4 import BeautifulSoup

apiurl = "https://a.4cdn.org/"
def parse(bot, user, channel, msg):
    for m in msg.split(' '):
        if m[:4] == "http" and '//' in m[5:-len(m)+8]:
            domain = m.split('/')[2].split('?')[0]
            if 'boards.4chan.org' in domain:
                try:
                    gr = re.compile(r'([a-zA-Z0-9]+)/res/([0-9]+)').search(m)
                    jo = json.loads(urllib2.urlopen(apiurl + gr.group(0) + '.json').read())["posts"]
                    info = "%s - %s%s | %s %s" % (
                        irc.SetColor(gr.group(1), irc.Color.Green),
                        irc.SetColor(("Anonymous" if not 'name' in jo[0] else netutil.unescape(jo[0]["name"])) ,irc.Color.Blue),
                        irc.SetColor(("" if not 'trip' in jo[0] else jo[0]['trip']), irc.Color.Yellow),
                        irc.SetColor('r:'+str(len(jo)), irc.Color.Red),
                        irc.SetColor('i:'+str(jo[0]["images"]), irc.Color.Red)
                    )
                    if 'sub' in jo[0]:
                        info += " | %s" % irc.Trunicate(netutil.unescape(jo[0]["sub"]))
                    if 'com' in jo[0]:
                        comment = BeautifulSoup(netutil.unescape(jo[0]["com"]).replace("<br>","\n")).text
                        comment = ' '.join([l if l[0] != '>' else irc.SetColor(l, irc.Color.Green) for l in comment.split('\n') if len(l) > 0])
                        info += " | " + irc.Trunicate(comment, 40)
                    bot.msg(channel, info)
                except Exception,e : print e


events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)
