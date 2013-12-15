# -*- coding: utf-8 -*-
#!/usr/bin/python

import urllib2
import json
import events
import re
import Util.irc as irc

apiurl = "https://gdata.youtube.com/feeds/api/videos/{VID}?alt=json&v=2"
def parse(bot, user, channel, msg):
    for m in msg.split(' '):
        if m[:4] == "http" and '//' in m[5:-len(m)+8]:
            domain = m.split('/')[2].split('?')[0]
            if 'youtube.' in domain:
                try:
                    vid = re.search(r"[A-Za-z0-9]{11}", m).group(0)
                    print apiurl.replace("{VID}", vid)
                    jo = json.loads(urllib2.urlopen(apiurl.replace("{VID}", vid)).read())
                    info = "%s %s %s %s | %s views" % (
                            irc.Bold(jo["entry"]["title"]["$t"][:30].rsplit(' ', 1)[0]+"..."), #trunicated
                            jo["entry"]["author"][0]["name"]["$t"],
                            irc.SetColor(jo["entry"]["yt$rating"]["numLikes"], irc.Color.Green),
                            irc.SetColor(jo["entry"]["yt$rating"]["numDislikes"], irc.Color.Red),
                            jo["entry"]["yt$statistics"]["viewCount"]
                    )
                    bot.msg(channel, info)
                except Exception,e: print e


events.setEvent('msg', 'youtube', parse)
print "youtube module loaded"