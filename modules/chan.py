# -*- coding: utf-8 -*-
#!/usr/bin/python

import urllib2
import json
import events
import re
import Util.irc as irc

regexes = {
    "thread" : re.compile(r"https?:/{2}boards\.4chan\.org\/([a-zA-Z0-9]+)/([0-9]+)")
}
apiurl = "https://a.4cdn.org/"
def parse(bot, user, channel, msg):
    for m in msg.split(' '):
        if m[:4] == "http" and '//' in m[5:-len(m)+8]:
            domain = m.split('/')[2].split('?')[0]
            if 'boards.4chan.org' in domain:
                try:
                    gr = regexes['thread'].search(m)
                    url = "%s/%s/%s" % (apiurl, gr.group(0), gr.group(1))
                    print url
                    jo = json.loads(urllib2.urlopen(url).read())
                    info = ""
                    bot.msg(channel, info)
                except Exception,e: print e


events.setEvent('msg', '4chan', parse)
print "4chan module loaded"