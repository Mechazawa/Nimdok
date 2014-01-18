# -*- coding: utf-8 -*-
#!/usr/bin/python
import urllib2
from bs4 import BeautifulSoup
from BotKit import command

@command("isup")
def parse(bot, channel, user, arg):
    if len(arg) == 0:
        bot.msg(channel, "%s: Usage, :isup [url]" % user)
    else:
        soup = BeautifulSoup(urllib2.urlopen("http://www.isup.me/" + urllib2.quote(arg)).read())
        response = soup.body.text.strip().split('\n')[0]
        bot.msg(channel, "%s: %s" % (user, response))