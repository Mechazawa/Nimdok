# -*- coding: utf-8 -*-

import urllib2
import json
import re
import HTMLParser
from bs4 import BeautifulSoup
from BotKit import handles, stylize


apiurl = "https://a.4cdn.org/"

@handles("msg")
def parse(bot, channel, user, msg):
    for m in msg.split(' '):
        if m[:4] == "http" and '//' in m[5:-len(m)+8]:
            domain = m.split('/')[2].split('?')[0]
            if 'boards.4chan.org' in domain:
                try:
                    gr = re.compile(r'([a-zA-Z0-9]+)/res/([0-9]+)').search(m)
                    jo = json.loads(urllib2.urlopen(apiurl + gr.group(0) + '.json').read())["posts"]
                    info = "%s - %s%s | %s %s" % (
                        stylize.SetColor(gr.group(1), stylize.Color.Green),
                        stylize.SetColor(("Anonymous" if not 'name' in jo[0] else unescape(jo[0]["name"])) , stylize.Color.Blue),
                        stylize.SetColor(("" if not 'trip' in jo[0] else jo[0]['trip']), stylize.Color.Yellow),
                        stylize.SetColor('r:'+str(len(jo)), stylize.Color.Red),
                        stylize.SetColor('i:'+str(jo[0]["images"]), stylize.Color.Red)
                    )
                    if 'sub' in jo[0]:
                        info += " | %s" % stylize.Trunicate(unescape(jo[0]["sub"]))
                    if 'com' in jo[0]:
                        comment = BeautifulSoup(unescape(jo[0]["com"]).replace("<br>","\n")).text
                        comment = ' '.join([l if l[0] != '>' else stylize.SetColor(l, stylize.Color.Green) for l in comment.split('\n') if len(l) > 0])
                        info += " | " + stylize.Trunicate(comment, 40)
                    bot.msg(channel, info)
                except Exception,e : print e

def unescape(s):
    return HTMLParser.HTMLParser().unescape(s)
