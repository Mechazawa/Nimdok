import urllib2
from bs4 import BeautifulSoup
from events import events 

def parse(bot, user, channel, msg):
	try:
		soup = BeautifulSoup(urllib2.urlopen(url))
		bot.msg(channel, soup.title.text.strip())
	except Exception: pass

events['msg'].append(parse)
print "urlinfo module loaded"