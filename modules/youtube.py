# -*- coding: utf-8 -*-
#!/usr/bin/python

import urllib2
import json
import events
import re
import Util.irc as irc
import Util.net as netutil
import Util.human as human

apiurl = "https://gdata.youtube.com/feeds/api/videos/{VID}?alt=json&v=2"
def parse(bot, user, channel, msg):
    for m in msg.split(' '):
        if m[:4] == "http" and '//' in m[5:-len(m)+8]:
            if 'youtube.' in netutil.getdomain(m) or 'youtu.be' in netutil.getdomain(m):
                vid = re.search(r"[A-Za-z0-9_-]{11}", m).group(0)
                jo = json.loads(urllib2.urlopen(apiurl.replace("{VID}", vid)).read())
                data = {
                    "views" : int(jo["entry"]["yt$statistics"]["viewCount"]),
                    "dislikes" : int(jo["entry"]["yt$rating"]["numDislikes"]),
                    "likes" : int(jo["entry"]["yt$rating"]["numLikes"]),
                    "author" :jo["entry"]["author"][0]["name"]["$t"],
                    "title" :jo["entry"]["title"]["$t"]
                }

                #TODO this needs some minor refactoring
                fmt = u"%s %s %s %s | %s views"
                info = fmt % (
                        irc.Bold(irc.Trunicate(data["title"])),
                        data["author"],
                        irc.SetColor(u"↑" + human.intcomma(data["likes"]), irc.Color.Green),
                        irc.SetColor(u"↓" + human.intcomma(data["dislikes"]), irc.Color.Red),
                        human.intcomma(data["views"]) if data["views"] < 1000000 else human.intword(data["views"])
                )
                bot.msg(channel, info.encode('utf-8', 'ignore'))


events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)