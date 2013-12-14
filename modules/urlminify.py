import urllib2
from events import events 

def parse(bot, user, channel, msg):
    if m[:4] == "http" and '//' in m[5:-len(m)+8]:
        if len(m) > 40:
           try:
               bot.msg(channel, urllib2.urlopen("http://tinyurl.com/api-create.php?url="+m).read())
           except Exception: pass   


events['msg'].append(parse)
print "urlminify module loaded"