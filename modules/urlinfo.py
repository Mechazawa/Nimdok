import urllib2
from bs4 import BeautifulSoup
import events

ignoreddomains = ["youtube.com"]
def parse(bot, user, channel, msg):
    for m in msg.split(' '):
        if m[:4] == "http" and '//' in m[5:-len(m)+8]:
            domain = m.split('/')[2].split('?')[0]
            domain = domain.split('.', domain.count(".")-1)[-1]
            if domain in ignoreddomains: continue
            try:
                soup = BeautifulSoup(urllib2.urlopen(m))
                bot.msg(channel, soup.title.text.strip())
            except Exception: pass

events.setEvent('msg', 'urlinfo', parse)
print "urlinfo module loaded"