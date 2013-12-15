import urllib2
import events

def parse(bot, user, channel, msg):
    for m in msg.split(' '):
        if m[:4] == "http" and '//' in m[5:-len(m)+8]:
            if len(m) > 40:
               try:
                   bot.msg(channel, urllib2.urlopen("http://tinyurl.com/api-create.php?url="+m).read())
               except Exception: pass   


events.setEvent('msg', 'urlminify', parse)
print "urlminify module loaded"