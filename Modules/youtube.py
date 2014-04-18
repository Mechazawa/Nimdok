# -*- coding: utf-8 -*-

import urllib2
import json
from re import compile

from BotKit import handles, stylize, humanize


#ytRegex = compile(r"""(?:youtube(?:-nocookie)?\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/ ]{11})""")
ytRegex = compile(r"youtu.+\W([A-Za-z0-9\-_]{11})(\W|$)")
apiurl = "https://gdata.youtube.com/feeds/api/videos/{VID}?alt=json&v=2"
@handles('msg')
def parse(bot, channel, user, msg):
    for m in msg.split(' '):
        if m[:4] == "http" and '//' in m[5:-len(m)+8]:
            if 'youtube.' in getdomain(m) or 'youtu.be' in getdomain(m):
                vid = ytRegex.search(m).group(1)
                bot.logger.info("Matched youtube id: %s" % vid)
                jo = json.loads(urllib2.urlopen(apiurl.replace("{VID}", vid)).read())
                data = {
                    "views" : int(jo["entry"]["yt$statistics"]["viewCount"]),
                    "dislikes" : int(jo["entry"]["yt$rating"]["numDislikes"]),
                    "likes" : int(jo["entry"]["yt$rating"]["numLikes"]),
                    "author" :jo["entry"]["author"][0]["name"]["$t"],
                    "title" :jo["entry"]["title"]["$t"]
                }

                fmt = u"%s %s %s %s | %s views"
                info = fmt % (
                        stylize.Bold(stylize.Trunicate(data["title"], 60)),
                        '| '+data["author"],
                        stylize.SetColor(u"↑" + humanize.intcomma(data["likes"]), stylize.Color.Green),
                        stylize.SetColor(u"↓" + humanize.intcomma(data["dislikes"]), stylize.Color.Red),
                        humanize.intcomma(data["views"]) if data["views"] < 1000000 else humanize.intword(data["views"])
                )
                bot.msg(channel, info.encode('utf-8', 'ignore'))


def getdomain(s, nosub=False):
    domain = s.split('/')[2].split('?')[0]
    return domain.split('.', domain.count(".")-1)[-1] if nosub else domain
