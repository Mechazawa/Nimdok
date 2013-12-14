import urllib2
from bs4 import BeautifulSoup
from events import events 

def parse(bot, user, channel, msg):
	if m[:4] == "http" and '//' in m[5:-len(m)+8]:
		try:
			soup = BeautifulSoup(urllib2.urlopen(m))
			bot.msg(channel, soup.title.text.strip())
		except Exception: pass

events['msg'].append(parse)
print "urlinfo module loaded"