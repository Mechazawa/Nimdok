# -*- coding: utf-8 -*-
#!/usr/bin/python

import events
import datetime

def parse(bot, user, channel, msg):
	with open('chat.log', 'a') as log:
		log.write("[%s] %s %s: %s\n" % (datetime.datetime.now().strftime("%m-%d %H:%M:%S"), channel, user, msg))

events.setEvent('msg', __file__[:-3].split('/')[-1].strip('.'), parse)